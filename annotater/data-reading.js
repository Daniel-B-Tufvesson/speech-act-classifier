/**
 * Some functions for reading text data.
 */

import { Sentence } from "./annotater.js";


/**
 * Generator function that yields each line in a file.
 * @generator
 * @param {string} fileURL 
 * @yields {string} the next line in the file.
 */
async function* lines(fileURL) {
    // Code taken from https://developer.mozilla.org/en-US/docs/Web/API/ReadableStreamDefaultReader/read#example_2_-_handling_text_line_by_line

    const utf8Decoder = new TextDecoder("utf-8");
    let response = await fetch(fileURL);
    let reader = response.body.getReader();
    let { value: chunk, done: readerDone } = await reader.read();
    chunk = chunk ? utf8Decoder.decode(chunk, { stream: true }) : "";
  
    let re = /\r\n|\n|\r/gm;
    let startIndex = 0;
  
    for (;;) {
        let result = re.exec(chunk);
        if (!result) {
            if (readerDone) {
                break;
            }
            let remainder = chunk.substr(startIndex);
            ({ value: chunk, done: readerDone } = await reader.read());
            chunk = remainder + (chunk ? utf8Decoder.decode(chunk, { stream: true }) : "");
            startIndex = re.lastIndex = 0;
            continue;
        }
        yield chunk.substring(startIndex, result.index);
        startIndex = re.lastIndex;
    }
    if (startIndex < chunk.length) {
      // last line didn't end in a newline char
      yield chunk.substr(startIndex);
    }
}


/**
 * Parse the first N sentences from a file. 
 * 
 * The file format should be like the following example:
 * 
 * 
 * @param {string} fileURL 
 * @param {number} nSentences the number of sentences to choose. -1 to read the entire file.
 * @returns {Array<Sentence>} an array of sentences.
 */
export async function parseSentences(fileURL, nSentences) {
    // The following is an example of the file format.
    //
    // sent_id = b6311d8
    // text = Ska man göra det?
    //
    // sent_id = b63ca38
    // text = DET är kul.
    //
    // Note how the sentences are separated by an empty line.


    const sentences = []

    let sentenceText = null
    let sentenceID = null
    let sentenceCount = 0
    for await (let line of lines(fileURL)) {

        // Parse sentence if empty line.
        if (line === '') {
            
            if (sentenceID !== null && sentenceText !== null) {
                let sentence = new Sentence(sentenceID, sentenceText)
                sentences.push(sentence)
                sentenceCount++

                // Stop if we have reached max sentences.
                if (sentenceCount == nSentences) {
                    break
                }
            }
        }
        // Parse text or ID.
        else {
            line = line.trim()

            // Parse sentence ID.
            if (line.startsWith('sent_id = ')) {
                sentenceID = line.substring('sent_id = '.length)
            }
            // Parse sentence text.
            else if (line.startsWith('text = ')) {
                sentenceText = line.substring('text = '.length)
            }
        }
    }

    return sentences
}

/**
 * Parse and retrieve a random sample of sentences from a file.
 * 
 * @param {string} fileURL 
 * @param {number} nSentences the number of sentences to choose.
 * @returns {Array<Sentence>} an array of sentences.
 */
export async function random_sample_of_sentences(fileURL, nSentences) {
    const sample = []
    const sentences = await parseSentences(fileURL, -1)

    // Choose N random sentences.
    for (let i = 0; i < nSentences; i++) {
        const index = randomRange(0, sentences.length)
        sample.push(sentences[index])
    }

    return sample
}


function randomRange(min, max) {
    return Math.floor(Math.random() * (max - min) + min)
}

