## Delay script example

Given an srt input file:

```
$ cat in.srt

1
00:07:41,557 --> 00:07:47,514
U heeft me te pakken.
- Welkom in de Haydi-Har-hut.

2
00:07:47,580 --> 00:07:51,292
Als we geen glimlach op uw gezicht kunnen
krijgen dan is uw huid te strak.
```

Run following python script to delay all titles in input file by 5 minutes and 43 seconds and write result
to out.srt:

```
$ python subdelay.py 05:43 in.srt out.srt

reading in.srt... done.
Delaying each line by 5 minutes and 43 seconds... done.
writing out.srt... done.

```

The output srt is now written to out.srt and you can see the intervals have been changed:

```
$ cat out.srt

1
00:13:24,557 --> 00:13:30,514
U heeft me te pakken.
- Welkom in de Haydi-Har-hut.

2
00:13:30,580 --> 00:13:34,292
Als we geen glimlach op uw gezicht kunnen
krijgen dan is uw huid te strak.
```

## Translations install dependencies

```
 python -m venv python_env
 source python_env/bin/activate
 pip install -r requirements.txt
```

## Example usage

```
python sub_translate.py fr in.srt french.srt

reading in.srt... done.
translating texts... 50.0% 100.0% done.
writing french.srt... done.
```
