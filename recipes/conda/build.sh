
sed -i.orig "s|#install_dir=build|install_dir=$PREFIX|" setup.cfg
git update-index --assume-unchanged setup.cfg

$PYTHON setup.py clean --all

export PYTHON_LDFLAGS=" "

$PYTHON setup.py build
$PYTHON setup.py install

# This headers are known to collide with astropy's extensions and would prevent astropy from building
rm -f $PREFIX/include/wcs*.h

