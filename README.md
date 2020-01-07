# grippy

Dead simple pure Python GRIB 2 data processing

## Running the tests

Because of the way that python 3 handles packages, you cannot run the test scripts directly. Instead run them as shown below:

```bash
cd /path/to/grippy
cd ../
python -m grippy.test_fetch.py
python -m grippy.test_wvper.py
```

If those run succesfully, you are good to go.