"""Regresión de la excepción de portada: nunca exime páginas interiores."""
import unittest
from convertir import evaluar_capa_texto

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

if __name__=='__main__':unittest.main()
