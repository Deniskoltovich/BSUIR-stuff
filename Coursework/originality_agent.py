import asyncio

import numpy as np
from PIL import Image
from neo4j import AsyncGraphDatabase


class OriginalityAgent:
    def __init__(self, driver):
        """
        :param driver: AsyncGraphDatabase driver
        """
        self.driver = driver

    # главный метод для запуска агента
    async def run(self, user_pic_path):
        """
        Берет картину (:Node) <-[:nrel_context]<-(cur: Node {name: 'current_request'})

                -[:nrel_belong_to]->(:Class {name: "concept_request"}) и сравнивает с картиной от пользователя

        Результат записывает в (:Node {name: "<originality percentage>"})
                <-[:nrel_originality] - (cur: Node {name: 'current_request'})
        USAGE:
                agent = OriginalityAgent(driver)

                await agent.run(user_pic_path='output_7_0.png')

        :param user_pic_path: Путь к картине от пользователя
        :return: None
        """
        pic_in_db_path = await self.get_pic_path_from_request(nrel_to_pic='nrel_context')
        with Image.open(pic_in_db_path) as img1:
            img1.load()
        with Image.open(user_pic_path) as img2:
            img2.load()

        img1, img2 = await OriginalityAgent.make_the_same_size(img1, img2)
        originality_percentage: str = await OriginalityAgent.evaluate_originality(img1, img2)

        async with self.driver.session() as session:
            await session.execute_write(OriginalityAgent.add_result_to_request_context, originality_percentage)

        return None

    @staticmethod
    async def add_result_to_request_context(tx, result: str):
        """
        Добавление результата к ноде current_request
        """

        await tx.run('''MATCH (req:Node {name: "current_request"})
                        CREATE (n:Node {name: "%s"})<-[:nrel_originality]-(req)
                     ''' % result)

    async def get_pic_path_from_request(self, nrel_to_pic: str = 'nrel_context'):
        """
        Получение пути к изображению в БЗ
        """
        get_pic_name = '''MATCH (req:Node {name: "current_request"})-[:%s]->(pic: Node) RETURN pic''' % nrel_to_pic

        get_pic_path = '''MATCH (n:Node {name: '%s'})
                            <-[:rrel_key_element]-(c:Node)-[:rrel_example]->(t: Text)
                            WHERE (c)-[:nrel_belong_to]->(:Class {name: "illustration"}) RETURN t'''
        async with self.driver.session() as session:
            pic_name = await session.execute_read(OriginalityAgent.execute_get_pic_name_query, get_pic_name)
            pic_path = await session.execute_read(OriginalityAgent.execute_get_pic_path_query, get_pic_path % pic_name)

        return pic_path

    @staticmethod
    async def evaluate_originality(left, right) -> str:
        """
        Подсчет оригинальности
        """
        img1 = left.convert("RGB")
        img2 = right.convert("RGB")

        left_array = np.asarray(img1)
        right_array = np.asarray(img2)

        left_array = left_array.astype(np.uint8)
        right_array = right_array.astype(np.uint8)

        difference_array = np.abs(right_array - left_array)

        different_pixels = np.count_nonzero(difference_array)
        total_pixels = left_array.size

        percentage_difference = (different_pixels / total_pixels) * 100
        return f'{100 -percentage_difference:.2f}%'

    @staticmethod
    async def make_the_same_size(img1, img2):
        width1, height1 = img1.size
        width2, height2 = img2.size

        new_width = min(width1, width2)
        new_height = min(height1, height2)

        img1 = img1.crop((0, 0, new_width, new_height))
        img2 = img2.crop((0, 0, new_width, new_height))
        return img1, img2

    @staticmethod
    async def execute_get_pic_name_query(tx, get_pic_name_query: str):
        pic_result = await tx.run(get_pic_name_query)
        pic_record = await pic_result.single()
        return pic_record.data()['pic']['name']

    @staticmethod
    async def execute_get_pic_path_query(tx, get_pic_path_query: str):
        pic_result = await tx.run(get_pic_path_query)
        pic_path = await pic_result.single()
        return pic_path.data()['t']['content']


async def main():
    uri = "neo4j://localhost:7687/test"
    driver = AsyncGraphDatabase.driver(uri, auth=("neo4j", "8512962den2004"))
    agent = OriginalityAgent(driver)
    async with driver.session(database='test') as session:
        await session.execute_write(lambda tx: tx.run('''MATCH (req:Class {name: "concept_request"})
                       CREATE (cur: Node {name: 'current_request'})-[:nrel_belong_to]->(req)'''))
    await driver.close()


if __name__ == '__main__':
    asyncio.run(main())
