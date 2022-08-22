#needs to be fixed

import aiohttp
import hikari

async def Paper_Tracker():
    url = 'https://api.coralcube.io/v1/getActivity?offset=0&page_size=25&activity_type=listings'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

    async with aiohttp.ClientSession() as session:
        urlRlCol = await session.get(url, headers=headers, ssl=False)
        allRlCol= await urlRlCol.json()
        prevChecked = []
        for recentListing in allRlCol:
            if not recentListing["key"] in prevChecked:
                async with aiohttp.ClientSession() as session2:
                    url2 = "https://api.coralcube.io/v1/getItems?offset=0&page_size=1&ranking=price_asc&symbol=" + str(recentListing["collection_symbol"])
                    urlColInfo = await session2.get(url2, headers=headers, ssl=False)
                    colData =await urlColInfo.json()
                    prevChecked.append(recentListing["key"])
                    try:
                        colInfo=colData['collection']
                    except:
                        print("Collection not Found")
                    else:
                        try:
                            floorPrice = colInfo["floor_price"]
                            floorPrice=floorPrice/1000000000

                        except:
                            print("Collection Error")
                        else:
                            phFp = floorPrice-((floorPrice*.12))
                            rlPrice = recentListing["price"]/1000000000
                            if rlPrice <= phFp:
                                yield recentListing
                print("Checking...")