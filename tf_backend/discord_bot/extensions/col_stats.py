
import requests
import json
from pyppeteer import launch
from pyppeteer_stealth import stealth
import hikari


#redo using other endpoints need fp, vol, and listed

#fp has current and past metrics of fp, use ME data collector 
#vol using coral cube shows current and past vol
#listed using coral cube has current and past listings

#https://stats-mainnet.magiceden.io/collection_stats/getCollectionTimeSeries/degentown?edge_cache=true&resolution=1h&addLastDatum=true
#this url can get all info but will take more manipulation

#https://api.coralcube.io/v1/getItems?offset=0&page_size=24&ranking=price_asc&symbol=primates
#less data overall but easier to use.


def ColStats(col):

    col_url = "https://api.coralcube.io/v1/getItems?offset=0&page_size=1&ranking=price_asc&symbol=" + str(col)
    headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'}  
    url_col_info = requests.get(col_url, headers=headers)
    collection_data = json.loads(url_col_info.text)

    url = "https://magiceden.io/marketplace/" + col
    col = col.replace("_", " ")
    col = col.title()

    stats_embed = hikari.Embed(
        title="**%s**" % (col),
        color="#996515",
        url=url,
    )
    stats_embed.set_footer(f"Toast or DIE")


    if "detail" in collection_data:
        stats_embed.add_field(
                            name="**Error**",
                            value="No Collection Found.",
                            inline=True
                        )

        return stats_embed
    else:
    
        col_stats = collection_data["collection"]
        col_img = col_stats["image"]
        
        morph = col_stats["stats"]

        
        sales_data = morph["sales"]
        total_sales = sales_data["total"]
        tot_vol = total_sales["volume"]/1000000000
        one_day_sales= sales_data["1d"]
        one_day_vol = one_day_sales["volume"]/1000000000
        seven_day_sales= sales_data["7d"]
        seven_day_vol=seven_day_sales["volume"]/1000000000
        thirty_day_sales= sales_data["30d"]
        thirty_day_vol=thirty_day_sales["volume"]/1000000000
        prev_one_day_sales= sales_data["prev_1d"]
        prev_one_day_vol=prev_one_day_sales["volume"]/1000000000
        prev_seven_day_sales= sales_data["prev_7d"]
        prev_seven_day_vol=prev_seven_day_sales["volume"]/1000000000
        prev_thirty_day_sales= sales_data["prev_30d"]
        prev_thirty_day_vol=prev_thirty_day_sales["volume"]/1000000000

        stats_embed.set_thumbnail(
            col_img
            )

        try:
            fp = col_stats["floor_price"]/1000000000
        except:
            fp = "NULL"
        else:
            stats_embed.add_field(
                            name="**Floor Price:**",
                            value="`"+str(fp)+"`",
                            inline=True
                        )
        try:
            tot_vol = col_stats["volume"]/1000000000
        except:
            tot_vol = "NULL"
        else:
            stats_embed.add_field(
                name="**Total Volume:**",
                value="`"+str(round(tot_vol, 2))+"`",
                inline=True
            )
        try:   
            listed_cnt = col_stats["listed_count"]
        except:
            listed_cnt = "NULL"
        else:
            stats_embed.add_field(
            name="**Listed:**",
            value="`"+str(listed_cnt)+"`",
            inline=True
        )


        stats_embed.add_field(
            name="**Vol 1D:**",
            value="`"+str(round(one_day_vol, 2))+"`",
            inline=True
        )
        
        stats_embed.add_field(
            name="**Vol 7D:**",
            value="`"+str(round(seven_day_vol, 2))+"`",
            inline=True
        )

        stats_embed.add_field(
            name="**Vol 30D:**",
            value="`"+str(round(thirty_day_vol, 2))+"`",
            inline=True
        )
        
        stats_embed.add_field(
            name="**Vol Prev 1D:**",
            value="`"+str(round(prev_one_day_vol, 2))+"`",
            inline=True
        )

        stats_embed.add_field(
            name="**Vol Prev 7D:**",
            value="`" +str(round(prev_seven_day_vol, 2))+"`",
            inline=True
        )
        
        stats_embed.add_field(
            name="**Vol Prev 30D:**",
            value="`" +str(round(prev_thirty_day_vol, 2))+"`",
            inline=True
        )

    return stats_embed

# async def HistStats(col, stats_embed):
#         prev_fp_url= "https://api-mainnet.magiceden.io/rpc/getAggregatedCollectionMetricsBySymbol?edge_cache=true&symbols=" + str(col)
        
#         # For docker
#         browser = await launch(executablePath='/usr/bin/google-chrome-stable', headless=True, args=['--no-sandbox'])
#         # For Development
#         # browser = await launch(headless=True)

#         page = await browser.newPage()

#         await stealth(page)
#         await page.goto(prev_fp_url)
#         content = await page.evaluate('document.body.textContent', force_expr=True)
#         hist_stats = json.loads(content)
#         await browser.close()
#         results_1 = hist_stats["results"]
#         results = results_1[0]
#         hist_fp = results["floorPrice"]
#         hist_vol = results["txVolume"]
#         print(hist_fp)
#         print(hist_vol)


#         try:
#             vol_delta_1h = hist_vol["delta1h"]

#         except:
#             vol_delta_1h = "None"

#         else:
#             stats_embed.add_field(
#                 name="**Vol CHANGE 1H:**",
#                 value="`"+str(round(vol_delta_1h, 2))+"`",
#                 inline=True
#             )
#         try:
#             vol_delta_1d = hist_vol["delta1d"]

#         except:
#             vol_delta_1d = "None"

#         else:
#             stats_embed.add_field(
#                 name="**Vol CHANGE 1D:**",
#                 value="`"+str(round(vol_delta_1d, 2))+"`",
#                 inline=True
#             )
#         try:
#             vol_delta_7d = hist_vol["delta7d"]

#         except:
#             vol_delta_7d = "None"

#         else:
#             stats_embed.add_field(
#             name="**Vol CHANGE 7D:**",
#             value="`"+str(round(vol_delta_7d, 2))+"`",
#             inline=True
#         )
#         try:
#             vol_delta_30d = hist_vol["delta30d"]

#         except:
#             vol_delta_30d = "None"

#         else:
#              stats_embed.add_field(
#                 name="**Vol CHANGE 30D:**",
#                 value="`"+str(round(vol_delta_30d, 2))+"`",
#                 inline=False
#             )
        

#         try:
#             one_hr = hist_fp["value1h"]
#         except:
#             one_hr = "None"
#         else:
#             stats_embed.add_field(
#                         name="**FP 1H:**",
#                         value="`"+str(round(one_hr, 2))+"`",
#                         inline=True
#                     )
#         try:
#             one_1d = hist_fp["value1d"]
#         except:
#             one_1d = "None"
#         else:
#             stats_embed.add_field(
#                         name="**FP 1D:**",
#                         value="`"+str(round(one_1d, 2))+"`",
#                         inline=True
#                     )
#         try:
#             seven_day = hist_fp["value7d"]
#         except:
#             seven_day = "None"
#         else:
#             stats_embed.add_field(
#                 name="**FP 7D:**",
#                 value="`"+str(round(seven_day, 2))+"`",
#                 inline=True
#             )
#         try:
#             thirty_day = hist_fp["value30d"]

#         except:
#             thirty_day = "None"

#         else:
#             stats_embed.add_field(
#                 name="**FP 30D:**",
#                 value="`"+str(round(thirty_day, 2))+"`",
#                 inline=False
#             )
#         try:
#             prev_one_hr = hist_fp["prev1h"]

#         except:
#             prev_one_hr = "None"

#         else:
#             stats_embed.add_field(
#                 name="**FP Prev 1H:**",
#                 value="`"+str(round(prev_one_hr, 2))+"`",
#                 inline=True
#             )
            
#         try:
#             prev_one_day = hist_fp["prev1d"]

#         except:
#             prev_one_day = "None"

#         else:
#             stats_embed.add_field(
#                 name="**FP Prev 1D:**",
#                 value="`"+str(round(prev_one_day, 2))+"`",
#                 inline=True
#             )
#         try:
#             prev_sev_day = hist_fp["prev7d"]

#         except:
#             prev_sev_day = "None"

#         else:
#             stats_embed.add_field(
#                 name="**FP Prev 7D:**",
#                 value="`"+str(round(prev_sev_day, 2))+"`",
#                 inline=True
#             )
            
#         try:
#             prev_thirty_day = hist_fp["prev30d"]

#         except:
#             prev_thirty_day = "None"

#         else:
#             stats_embed.add_field(
#                 name="**FP Prev 30D:**",
#                 value="`" +str(round(prev_thirty_day, 2))+"`",
#                 inline=False
#             )
            
#         try:
#             fp_delta_1h = hist_fp["delta1h"]

#         except:
#             fp_delta_1h = "None"

#         else:
#             stats_embed.add_field(
#                 name="**FP CHANGE 1H:**",
#                 value="`"+str(round(fp_delta_1h, 2))+"`",
#                 inline=True
#             )
#         try:
#             fp_delta_1d = hist_fp["delta1d"]

#         except:
#             fp_delta_1d = "None"

#         else:
#             stats_embed.add_field(
#                 name="**FP CHANGE 1D:**",
#                 value="`"+str(round(fp_delta_1d, 2))+"`",
#                 inline=True
#             )
            
#         try:
#             fp_delta_7d = hist_fp["delta7d"]

#         except:
#             fp_delta_7d = "None"

#         else:
#             stats_embed.add_field(
#                 name="**FP CHANGE 7D:**",
#                 value="`" +str(round(fp_delta_7d, 2))+"`",
#                 inline=True
#             )
            
#         try:
#             fp_delta_30d = hist_fp["delta30d"]

#         except:
#             fp_delta_30d = "None"

#         else:
#             stats_embed.add_field(
#                 name="**FP CHANGE 30D:**",
#                 value="`"+str(round(fp_delta_30d, 2))+"`",
#                 inline=False
#             )

        

        
#         # current = histFP["current"]
#         # statsEmbed.add_field(
#         #     name="Magic Eden",
#         #     value=colURL,
#         # )
#         # statsEmbed.add_field(
#         #     name="Coral Cube",
#         #     value=col2URL,
#         # )
    
#         return stats_embed

