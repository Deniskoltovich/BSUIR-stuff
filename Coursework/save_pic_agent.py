import asyncio

from neo4j import AsyncGraphDatabase

# GET_PIC_PATH = '''MATCH (n:Node {name: '%s'})
#                     <-[:rrel_key_element]-(c:Node)-[:rrel_example]->(t: Text)
#                     WHERE (c)-[:nrel_belong_to]->(:Class {name: "illustration"})'''
#
#
# async def get_monalisa_node(tx):
#     result = await tx.run("MATCH (n:Node {name: 'test'}) RETURN n")
#     return await result.fetch(111)
#
#
# async def get_monalisas_rel_nodes(tx):
#     result = await tx.run('MATCH (n:Node {name: "Mona Lisa"})-[]->(c) RETURN c')
#     return await result.fetch(4)
#
#
# async def get_pic_path(tx, pic_name):
#     result = await tx.run(GET_PIC_PATH % pic_name + 'RETURN t')
#     return await result.fetch(1)
#
#
# async def set_pic_path(tx, pic_name, pic_path):
#     result = await tx.run(GET_PIC_PATH % pic_name + 'SET t.content = "%s" ' % pic_path + 'RETURN t')
#     return await result.fetch(1)


class SavePictureAgent:
    def __init__(self, driver):
        """
        :param driver: AsyncGraphDatabase driver
        """
        self.driver = driver

    async def run(
            self,
            name: str,
            path: str,
            statement: str = None,
            author: str = None,
            author_statement: str = None
    ):
        """
        USAGE:
            agent = SavePictureAgent(driver)

            await agent.run(name='Картина', path='./path2.jpg', statement='ОПИСАНИЕ КАРТИНЫ',
                            author='АВТОР', author_statement= 'ОПИСАНИЕ АВТОРА')

        :param name: Название картины
        :param path: Относительный или абсолютный локальный путь к изображению
        :param statement: Описание картины
        :param author: Имя автора картины
        :param author_statement: Информация об авторе
        :return: None
        """

        async with self.driver.session() as session:
            await session.execute_write(self.save_picture, name, path, statement, author, author_statement)
            await session.execute_write(self.add_result_to_request_context, name)
        return None

    @staticmethod
    async def save_picture(
            tx,
            name: str,
            path: str,
            statement: str = None,
            author: str = None,
            author_statement: str = None
    ):
        create_picture_query: str = await SavePictureAgent.make_picture_query(name, path, statement)
        author_data = await SavePictureAgent.make_author_query(author, author_statement) if author else ''

        result = await tx.run(create_picture_query + author_data)



        return list(await result.fetch(5))

    @staticmethod
    async def make_picture_query(name: str, path: str, statement: str):
        create_concept_entity = '''MATCH (c:Class {name: 'concept_picture'})
        CREATE (n:Node {name: '%s'})
        -[:nrel_belong_to]->(c)
        ''' % name

        create_pic_entity = '''CREATE (p:Node {name: 'Pic. (%s)'})
        -[:rrel_key_element]->(n)
        WITH p
        ''' % name

        create_nrel_with_illustration = '''MATCH (class:Class {name: "illustration"})
        CREATE (p)-[:rrel_example]->(class)
        '''

        create_pic_path = '''CREATE (p)
        -[:rrel_example]->(t1:Text {content: "%s"})
        WITH t1
        ''' % path

        create_pic_statement = ''
        if statement:
            create_pic_statement = '''MATCH (state:Class {name: 'statement'}) , (n:Node {name: '%s'})
            CREATE (st:Node {name: "St. (%s)"})
            -[:nrel_belong_to]->(state)
            CREATE (st)-[:rrel_key_element]->(n)
            CREATE (st)-[:rrel_example]->(t2:Text {content: "%s"})
            ''' % (name, name, statement)

        return (create_concept_entity + create_pic_entity +
                create_nrel_with_illustration + create_pic_path +
                create_pic_statement)

    @staticmethod
    async def add_result_to_request_context(tx, pic_name: str):
        await tx.run('''MATCH (n:Node {name: "%s"}), (req:Class {name: "concept_request"})
                        CREATE (n)<-[:nrel_context]-(req)
                     ''' % (pic_name))

    @staticmethod
    async def make_author_query(author: str, author_statement: str):
        create_pic_nrel_with_author = '''MERGE (author:Node {name: "%s"})
        CREATE (n)<-[:nrel_write]-(author)
        ''' % author

        create_autor_statement = ''
        if author_statement:
            create_autor_statement = '''CREATE (author)
            -[:rrel_key_element]->(stauthor:Node {name: "St. (%s)"})
            WITH author, stauthor
            ''' % author

            create_autor_statement += '''MATCH (state:Class {name: 'statement'})
            CREATE (stauthor)-[:nrel_belong_to]->(state)
            WITH stauthor
            '''

            create_autor_statement += '''CREATE (stauthor)
            -[:rrel_example]->(t3:Text {content: "%s"})
            ''' % author_statement

        return create_pic_nrel_with_author + create_autor_statement


async def main():
    uri = "neo4j://localhost:7687/test"
    driver = AsyncGraphDatabase.driver(uri, auth=("neo4j", "8512962den2004"))
    # async with driver.session(database='test') as session:
    #     await session.execute_write(set_pic_path, 'Mona Lisa', './output_6_0.png')
    agent = SavePictureAgent(driver)
    await agent.run(name='Картина2', path='./path2.jpg', statement='ОПИСАНИЕ2', author='АВТОР', author_statement='OGBCFYB')
    await driver.close()


if __name__ == '__main__':
    asyncio.run(main())
