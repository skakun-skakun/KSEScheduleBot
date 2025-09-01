import aiohttp
import asyncio
from pprint import pprint


class ApiParser:
    def __init__(self, url):
        self.domain_url = url

    async def parse_subject(self, subject, date_start, date_finish):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.domain_url, params={'from': date_start, 'till': date_finish, 'discipline': subject}) as resp:
                if resp.status == 200:
                    return await resp.json()
                else:
                    return resp.status

    @staticmethod
    async def _parse_group_from_subject_json(subject_json, group):
        pprint({'events': [[event
                            for event in day
                            if event.get('subgroup') == group]
                           if day is not None
                           else []
                           for day in subject_json['events']]})
    
    async def parse_group(self, subject, group, date_start, date_finish):
        return await self._parse_group_from_subject_json(await self.parse_subject(subject, date_start, date_finish), group)

    async def parse_course(self, group):
        pass


if __name__ == '__main__':
    parser = ApiParser('https://api.kse.today/schedule')
    asyncio.run(parser.parse_group('ECON201', 1, '2025-09-01', '2025-09-06'))
