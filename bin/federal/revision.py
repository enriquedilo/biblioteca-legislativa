import json,re,subprocess,collections,sys
from pathlib import Path
from PIL import Image,ImageDraw
from pypdf import PdfReader
root=Path('Federal');items=json.load(open(root/'reportes/piloto_resultados.json'));out=[];images=[]
for r in items:
 d=root/'ordenamientos'/str(r['id'])/'actual';v=json.load(open(d/'validacion.json'));m=json.load(open(d/'metadata.json'));pages=(d/'extraccion.txt').read_text().split('\f');reader=PdfReader(d/'original.pdf'); counts=[]
 for n,p in enumerate(reader.pages,1):
  counts.append(collections.Counter(re.findall(r'\d+',pages[n-1]))==collections.Counter(re.findall(r'\d+',p.extract_text() or '')))
 samples=sorted(set([1,next((x['pagina'] for x in v['encabezados_transitorios']),len(reader.pages)),len(reader.pages)]))
 for n in samples:
  prefix=Path('work/piloto_visual')/f"{r['sigla']}-{n}"
  subprocess.run(['pdftoppm','-f',str(n),'-l',str(n),'-singlefile','-scale-to','1100','-png',str(d/'original.pdf'),str(prefix)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
  img=Image.open(str(prefix)+'.png').convert('RGB');img.thumbnail((420,580));tile=Image.new('RGB',(440,620),'white');tile.paste(img,(10,30));ImageDraw.Draw(tile).text((10,10),f"{r['sigla']} pagina {n}",fill='black');images.append(tile)
 out.append({'sigla':r['sigla'],'paginas':v['paginas_pdf'],'texto_conservado':v['texto_conservado'],'listas_conservadas':all(x['inicios_lista_conservados'] for x in v['controles_por_pagina']),'paginas_cifras_mismo_multiconjunto':sum(counts),'paginas_cifras_diferentes':[n for n,b in enumerate(counts,1) if not b],'notas':len(m['reformas']),'po':m['po_publicacion'],'ultima':m['ultima_reforma'],'nombre':m['nombre_oficial'],'word':v['formato_word_original'],'samples':samples})
canvas=Image.new('RGB',(440*3,620*4),'#dddddd')
for i,img in enumerate(images):canvas.paste(img,((i%3)*440,(i//3)*620))
canvas.save('work/piloto_visual/contacto.png');Path('work/resumen.json').write_text(json.dumps(out,ensure_ascii=False,indent=2));print(json.dumps(out,ensure_ascii=False))
