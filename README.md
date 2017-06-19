## pbar
A configurable progress bar for the linux terminal.

## Usage 
Very simple and easy to use.

### basic
```python
bar = pbar()
bar.set_message('Counting to 1000...')

for i in range(1, 1001):
    bar.update(i, 1000)
    time.sleep(0.1)
```

### output
```
Counting to 1000...             [####################--------------------] 50.0%
```

### timer
```python
tbar = timed_pbar(time=20)
tbar.start()
```

### output
```
11.8s                           [########################----------------]  59.0%
```
