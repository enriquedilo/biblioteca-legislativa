"""Casos observados en los IDs 116 y 120; sin alterar el texto impreso."""
import sys, unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from indices import articulos_de

class IndicesInternos(unittest.TestCase):
 def test_dos_puntos(self):
  texto='<!-- PAGINA_PDF: 6 -->\n### Artículo 9.\nDictamen.\n### Artículo 10:\nLa opinión técnica.\n'
  arts=articulos_de(texto)
  self.assertEqual([a['articulo'] for a in arts],['9','10'])
  self.assertIn('Artículo 10:',arts[1]['_texto'])
 def test_cuerpo_por_secciones_y_transitorios(self):
  texto='<!-- PAGINA_PDF: 1 -->\nProtocolo\n<!-- PAGINA_PDF: 2 -->\nMedidas de accesibilidad.\n## TRANSITORIOS\nPRIMERO. Se creará un comité.\nSEGUNDO. Plazo de ejecución.\n'
  arts=articulos_de(texto)
  self.assertEqual([a['tipo'] for a in arts],['seccion','seccion','transitorio','transitorio'])
  self.assertIn('Medidas de accesibilidad.',arts[1]['_texto'])
  self.assertNotIn('PRIMERO.',arts[1]['_texto'])
  self.assertTrue(all(a['linea_fin']<b['linea_inicio'] for a,b in zip(arts,arts[1:])))
 def test_articulado_no_recibe_secciones(self):
  arts=articulos_de('<!-- PAGINA_PDF: 1 -->\n### Artículo 1.\nTexto.\n## TRANSITORIOS\nÚNICO. Vigencia.\n')
  self.assertEqual([a['tipo'] for a in arts],['cuerpo','transitorio'])

if __name__=='__main__':unittest.main()
