from motor.motor_asyncio import AsyncIOMotorClient
from aiogram.fsm.storage.base import BaseStorage, StorageKey, StateType



# State storage class that uses mongodb and can be passed to dispatcher
class MongoStorage(BaseStorage):
    def __init__(self, db_uri, db_name='', collection_name=''):
        self._db_uri = db_uri
        self._db_name = db_name
        self._collection_name = collection_name
        self._client = AsyncIOMotorClient(self._db_uri)
        self._db = self._client[self._db_name]
        self._collection = self._db[self._collection_name]

    # ----- Base methods ----------------
    # set state base function
    async def set_state(self, key: StorageKey, state: StateType) -> None:
        print('Set state')
        result = await self._collection.find_one({'user_id': key.user_id})
        if not result:
            await self._collection.insert_one({'chat_id': key.chat_id, 'user_id': key.user_id, 'state': state.state})
        else:
            await self._collection.update_one({'user_id': key.user_id}, {'$set': {'state':state.state}})

    # get state base function
    async def get_state(self, key: StorageKey):
        print('Get state')
        result = await self._collection.find_one({'user_id': key.user_id})
        if result:
            return result.get('state')
        else:
            return None
    # set data base function
    async def set_data(self, key: StorageKey, data: dict | None = None):
        print('Set data')
        await self._collection.update_one({'user_id': key.user_id}, {'$set': {'data': data}})

    async def get_data(self, key: StorageKey):
        print('Get data')
        result = await self._collection.find_one({'user_id': key.user_id})
        if result:
            return result.get('data')
        else:
            return None

    async def update_data(self, key: StorageKey, data: dict | None = None):
        print('Update data')
        result = await self._collection.find_one({'user_id': key.user_id})
        data_to_update = result.get('data')

        if data_to_update:
            data_to_update.update(data)
        else:
            data_to_update = data
        await self._collection.update_one({'user_id':key.user_id}, {'$set': {'data': data_to_update}})
    async def wait_closed(self):
        pass

    async def close(self):
        await self._client.close()

    # ----------- Extended methods ------

    async def get_all_data(self, query: dict):
        print('Get all data')
        cursor = self._collection.find(query)
        result = await cursor.to_list(None)
        return result

    async def get_one(self, query: dict):
        print('Get one')
        result = await self._collection.find_one(query)
        return result

    async def update_certain_data(self, query: dict, data: dict):
        print('Update certain data')
        result = await self._collection.find_one(query)
        print(result)
        data_to_update = result.get('data')
        print(data)
        if data_to_update:
            data_to_update.update(data)
        else:
            data_to_update = data
        print(data_to_update)
        await self._collection.update_one(query, {'$set': {'data': data_to_update}})
