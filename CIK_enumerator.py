import asyncio
import aiohttp
import time as t

headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64)'}
async def existence(cik, session, out):
    try:
        link = "https://www.sec.gov/Archives/edgar/data/"+ str(cik) +"/"
        async with session.get(link, headers=headers, timeout=5) as page:
            if page.status == 200:
                out.write(str(cik) + "\n")
                return str(cik)
            else:
                return
    except Exception:
        print("Retrying: " + str(cik))
        await existence(cik, session, out)


async def main():
    output = open("CIKs.txt", "w+")
    for cik in range(1, 10000000, 10):
        if int(cik)%10000 == 0:
            print("Wow this far: " + cik)     

        urls = []
        for i in range(10):
            urls.append(cik+i)

        async with aiohttp.ClientSession() as sess:
            tasks = []
            for url in urls:
                task = asyncio.create_task(existence(url, sess, output))
                tasks.append(task)
        
            responses = await asyncio.gather(*tasks)
            for rep in responses:
                if rep != None:
                    print(rep)
            

    print("Holy Shit?")
    output.close() 

asyncio.run(main())

#https://www.sec.gov/ix?doc=/Archives/edgar/data/ /
'''
If a user or application submits more than 10 requests per second to EDGAR websites, the SEC may limit further
 requests from the relevant IP address(es) for a brief period. When the rate of requests drops below the 10-requests-per-second
 threshold, the user will be able to resume access to these websites. This practice is designed to limit excessive automated searches
 and is not intended or expected to impact use by individuals.
'''
