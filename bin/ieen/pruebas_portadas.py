"""Regresión de las cuatro clases de páginas sin texto; nunca OCR."""
import unittest
from convertir import evaluar_capa_texto, sin_texto_sustantivo

class Portadas(unittest.TestCase):
 def test_criterio(self):
  review={'pdf_sha256':'abc','nombre_oficial':'Título cotejado','portada':{'pagina_pdf':1,'cotejo_visual':True,'contiene_texto_normativo':False}}
  cases=[([],None,'abc',True),([1],review,'abc',True),([1],None,'abc',False),([1],review,'otro',False),([2],review,'abc',False),([1,7,18,20],review,'abc',False),([1,2,3,4,5],review,'abc',False)]
  for pages,rev,sha,expected in cases:
   with self.subTest(pages=pages,sha=sha,revision=rev):self.assertEqual(evaluar_capa_texto(pages,rev,sha)['promover'],expected)
  for field,value in [('cotejo_visual',False),('contiene_texto_normativo',True),('contiene_texto_normativo',None),('pagina_pdf',2)]:
   changed={**review,'portada':{**review['portada'],field:value}}
   with self.subTest(field=field,value=value):self.assertFalse(evaluar_capa_texto([1],changed,'abc')['promover'])
  self.assertFalse(evaluar_capa_texto([1],{**review,'nombre_oficial':None},'abc')['promover'])

class CapaTexto(unittest.TestCase):
 def test_marca_de_agua_no_es_cuerpo(self):
  self.assertTrue(sin_texto_sustantivo('Cop     ia de I    nter     net'))
  self.assertFalse(sin_texto_sustantivo('Copia de Internet\nArtículo 1. El Instituto tendrá las siguientes atribuciones.'))
 def test_tabla_numerica_no_se_descarta(self):
  self.assertFalse(sin_texto_sustantivo('1000 2000 3000 4000 5000 6000'))



class CuatroCasos(unittest.TestCase):
 def revision(self,caso,visual=True):
  return {'pdf_sha256':'abc','nombre_oficial':'Título','paginas_sin_texto':{'2':{'pagina_pdf':2,'caso':caso,'cotejo_visual':visual,'evidencia':'Cotejo de prueba'}}}
 def test_clasificacion(self):
  for caso,ok in [('blanca',True),('grafica',True),('texto_normativo_imagen',False),('revision_pendiente',False)]:
   with self.subTest(caso=caso):self.assertEqual(evaluar_capa_texto([2],self.revision(caso),'abc')['promover'],ok)
  self.assertFalse(evaluar_capa_texto([2],self.revision('grafica',False),'abc')['promover'])
  self.assertFalse(evaluar_capa_texto([2],self.revision('grafica'),'otro')['promover'])
 def test_render_blanco_y_trazos(self):
  import tempfile
  from pathlib import Path
  from pypdf import PdfWriter
  from pypdf.generic import DecodedStreamObject,NameObject
  from convertir import detectar_blancas
  with tempfile.TemporaryDirectory() as tmp:
   p=Path(tmp)/'prueba.pdf';w=PdfWriter();w.add_blank_page(width=72,height=72)
   page=w.add_blank_page(width=72,height=72);stream=DecodedStreamObject();stream.set_data(b'0 g 10 10 1 1 re f');page[NameObject('/Contents')]=w._add_object(stream)
   with p.open('wb') as f:w.write(f)
   auto=detectar_blancas(p,[1,2])
   self.assertEqual(auto['1']['caso'],'blanca');self.assertEqual(auto['2']['caso'],'revision_pendiente')
   self.assertTrue(evaluar_capa_texto([1],None,'abc',auto)['promover'])
   self.assertFalse(evaluar_capa_texto([2],None,'abc',auto)['promover'])

if __name__=='__main__':unittest.main()
