import asyncio
import aiohttp
import os
import time
import argparse

parser = argparse.ArgumentParser(description='async download ncbi description')
parser.add_argument("--data_file", default="data.txt")
parser.add_argument("--run_name", default="run")

args = parser.parse_args()

def get_gene_list(args):
    with open(args.data_file) as f:
        embids = []
        gene_ids = []
        f.readline()
        i = 0
        while f:
            line = f.readline()
            if line == "":
                break
            else:
                gene_id = line.split("\t")[1]
                embid = line.split("\t")[0]
                if ";" in gene_id:
                    gene_id = gene_id.split(";")
                    for gid in gene_id:
                        gid.replace(" ", "")
                        gene_ids.append(gid)
                        embids.append(embid)
                elif "-" not in gene_id:
                    gene_id.replace(" ", "")
                    gene_ids.append(gene_id)
                    embids.append(embid)
            i += 1
         
    assert len(gene_ids) == len(embids) 
    return gene_ids, embids

url = 'https://www.ncbi.nlm.nih.gov/gene/{}'

# read gene id 
gene_ids, embids = get_gene_list(args)

results = []
not_foud_list = []
not_found_ens_list = []
# time
start = time.time()

def post_process(html_str, url):
    try:
        html_str = html_str.split("<dt>Summary</dt>")[1].split("<dt>Expression</dt>")[0]
        html_str = html_str.split("<dd>")[1].split("</dd>")[0]
    except IndexError:
        print(f"error for request {url} - can't parse")
        html_str = "--- 404 ---"
        print("--- 404 ---")
    return html_str

async def read_urls(session, url, gene, emb_id):
    async with session.get(url) as resp:
        html_content = await resp.read()
        print(f"processing gene id {gene} ...")
        html_content = post_process(str(html_content), url)
        if html_content == "--- 404 ---":
            not_foud_list.append(gene)
            not_found_ens_list.append(emb_id)
        return html_content

def get_tasks(session):
    tasks = []
    for index, gene in enumerate(gene_ids):
        emb_id = embids[index]
        tasks.append(asyncio.create_task(read_urls(session, url.format(gene), gene, emb_id)))
    return tasks

async def get_results():
    connector = aiohttp.TCPConnector(force_close=True)
    async with aiohttp.ClientSession(connector=connector) as session:
        
        tasks = get_tasks(session)
        responses = await asyncio.gather(*tasks)
        for resp in responses:
            results.append(resp)
asyncio.run(get_results())

end = time.time()
total_time = end - start
print("It took {} seconds to make {} API calls".format(total_time, len(gene_ids)))


with open(f"{args.run_name}_results.txt", 'w') as f:
    f.write("emsbl_ID\tgene_id\tdesciption\n")
    for index, i in enumerate(results):
        f.write(f"{embids[index]}\t{gene_ids[index]}\t{i}\n")

with open(f"{args.run_name}_exceptions.txt", 'w') as f:
    f.write("Ensembl Gene ID\tGene ID\n")
    for index, i in enumerate(not_foud_list):
        f.write(f"{not_found_ens_list[index]}\t{i}\n")


print("Results writen into results.txt & exceptions to exceptions.txt")
