from distutils.core import setup
import setup_translate


setup(name = 'enigma2-plugin-extensions-openmultiboot',
		version='1.8',
		author='Dimitrij',
		author_email='dima-73@inbox.lv',
		package_dir = {'Extensions.OpenMultiboot': 'src'},
		packages=['Extensions.OpenMultiboot'],
		package_data={'Extensions.OpenMultiboot': ['plugin.png', 'readme', 'ubi_reader/*.py', 'ubi_reader/ubi/*.py', 'ubi_reader/ui/*.py', 'ubi_reader/ubi_io/*.py', 'ubi_reader/ubifs/*.py', 'ubi_reader/ubifs/lzo.so', \
			'ubi_reader/ubifs/nodes/*.py', 'ubi_reader/ubi/volume/*.py', 'ubi_reader/ubi/headers/*.py', 'ubi_reader/ubi/block/*.py']},
		description = 'Multi boot loader manager for enigma2 box',
		cmdclass = setup_translate.cmdclass,
	)

