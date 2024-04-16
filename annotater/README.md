# The Annotator
To manually annotate sentences, I developed a basic annotation tool.

## Running the Tool
The tool should be run locally hosted in a web browser. I recommend running it by using Live Server in VSCode. In VSCode, right click on `annotater-session.html` and click on "Open with Live Server".

To choose a data file to annotate, you must change the `fileURL` variable in the `annotater.js` script.

```js
...
// Read sentences from a file.
const fileURL = `test sentences no IDs.💬` // Change this to load other file.
const sentences = await parseSentences(fileURL, -1)
...

```

Once you have annotated all sentences in the file, it will automatically be downloaded to your `Downloads` directory.

## Input Data
The input data should be on the following format, where each sentence is separated by an empty line, sentence ID `sent_id` to identify the sentence, and the `text` which contains the text string to display in the tool:
```
# sent_id = 1300467
# text = jag kanske inte tillför nåt nytt. 

# sent_id = 500219
# text = Genom att kompostera komposterbara saker? 

# sent_id = 1100910
# text = tack för ditt svar! 
```

Or alternatively without sencence IDs:
```
# text = jag kanske inte tillför nåt nytt. 

# text = Genom att kompostera komposterbara saker? 

# text = tack för ditt svar! 
```

I have used .💬 as the file extension for these files, but any file extension should work as long as the file format is text.

## Output Data
Once you have annotated all sentences, the tool will produce an output file on the following format:

```
# sent_id = 1300467
# text = jag kanske inte tillför nåt nytt. 
# speech_act = assertion

# sent_id = 500219
# text = Genom att kompostera komposterbara saker?
# speech_act = question

# sent_id = 1100910
# text = tack för ditt svar! 
# speech_act = expressive
```

Or alternatively without sentence IDs:
```
# text = jag kanske inte tillför nåt nytt. 
# speech_act = assertion

# text = Genom att kompostera komposterbara saker?
# speech_act = question

# text = tack för ditt svar! 
# speech_act = expressive
```

These files will have the file extension .✏️ and the file format is text.