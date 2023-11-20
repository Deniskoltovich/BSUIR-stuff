import asyncio

from neo4j import AsyncGraphDatabase


class SavePictureAgent:
    def __init__(self, driver):
        """
        :param driver: AsyncGraphDatabase driver
        """
        self.driver = driver

    async def run(
            self,
            author_statement: str = None
    ):

        async with self.driver.session(database='test') as session:
            exc = await session.execute_read(self.check_if_pic_exists)
            try:
                exc.data()
                return False
            except:
                print('hhdsj')
                pass

            try:
                author = await session.execute_read(self.get_author_name)
                author = author.data()['req_author']['content']
            except AttributeError:
                author = None

            pic_name = await session.execute_read(self.get_pic_name)
            name = pic_name.data()['req_name']['content']

            pic_path = await session.execute_read(self.get_pic_path)
            path = pic_path.data()['req_url']['name']
            try:
                desc = await session.execute_read(self.get_desc)
                statement = desc.data()['req_desc']['name']
            except AttributeError:
                statement = None

            await session.execute_write(self.save_picture, name, path, statement, author, author_statement)
            await session.execute_write(self.add_result_to_request_context, name)
        return True

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
        author_data = await SavePictureAgent.make_author_query(author, author_statement, name) if author else ''

        result = await tx.run(create_picture_query + author_data)

        return list(await result.fetch(5))

    @staticmethod
    async def get_author_name(tx):
        res = await tx.run('''
                MATCH (cur: Node {name: 'current_request'})-[:nrel_author]->(req_author:Text) RETURN req_author
        ''')
        return await res.single()

    @staticmethod
    async def check_if_pic_exists(tx):
        res = await tx.run('''
            MATCH (cur: Node {name: 'current_request'})-[l:nrel_context]->(n:Node) RETURN n
        ''')

        return await res.single()

    @staticmethod
    async def get_desc(tx):
        res = await tx.run('''
                MATCH (cur: Node {name: 'current_request'})-[:nrel_description]->(req_desc:Text) RETURN req_desc
        ''')
        return await res.single()

    @staticmethod
    async def get_pic_name(tx):
        res = await tx.run('''
                MATCH (cur: Node {name: 'current_request'})-[:nrel_title]->(req_name:Text) RETURN req_name
        ''')
        return await res.single()

    @staticmethod
    async def get_pic_path(tx):
        res = await tx.run('''
                MATCH (cur: Node {name: 'current_request'})-[:nrel_url]->(req_url:Text) RETURN req_url
        ''')
        return await res.single()

    @staticmethod
    async def add_result_to_request_context(tx, pic_name: str):
        await tx.run('''MATCH (n:Node {name: "%s"}), (req:Node {name: "current_request"})
                        CREATE (n)<-[:nrel_context]-(req)
                     ''' % (pic_name))

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
            create_pic_statement = '''MATCH (state:Class {name: 'statement'}) , (n:Node {name: '%s'})-[:nrel_belong_to]->()
            CREATE (st:Node {name: "St. (%s)"})
            -[:nrel_belong_to]->(state)
            CREATE (st)-[:rrel_key_element]->(n)
            CREATE (st)-[:rrel_example]->(t2:Text {content: "%s"})
            ''' % (name, name, statement)

        return (create_concept_entity + create_pic_entity +
                create_nrel_with_illustration + create_pic_path +
                create_pic_statement)

    @staticmethod
    async def make_author_query(author: str, author_statement: str, pic_name: str):
        create_pic_nrel_with_author = '''MERGE (author:Node {name: "%s"}) WITH author
         MATCH (ar: Class {name:'concept_artist'}), (n:Node {name: '%s'})
        CREATE (n)<-[:nrel_write]-(author)-[:nrel_belong_to]->(ar)
        ''' % (author, pic_name)

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


async def start_save_picture_agent():
    uri = "bolt://localhost:7687"
    driver = AsyncGraphDatabase.driver(uri, auth=("Vlad", "Smolnik2904"), database='test')
    agent = SavePictureAgent(driver)
    await agent.run()
    await driver.close()

# if __name__ == '__main__':
#     asyncio.run(main())