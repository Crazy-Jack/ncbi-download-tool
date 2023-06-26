# with open("data.txt") as f:
#     embids = []
#     gene_ids = []
#     f.readline()
#     while f:
#         line = f.readline()
#         if line == "":
#             break
#         else:
#             gene_id = line.split("\t")[1]
#             embid = line.split("\t")[0]
#             if ";" in gene_id:
#                 gene_id = gene_id.split(";")
#                 for gid in gene_id:
#                     gene_ids.append(gid)
#                     embids.append(embid)
#             elif "-" not in gene_id:
#                 gene_ids.append(gene_id)
#                 embids.append(embid)

# assert len(gene_ids) == len(embids)

wl = ['001', '002']
fe = ['r2', 'u4b3']

with open("hellp", 'w') as f:
    for index, i in enumerate(wl):
        f.write(f"{i}\t{fe[index]}\n")