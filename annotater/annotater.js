/**
 * The main js code for the annotater.
 */

import { parseSentences } from "./data-reading.js"

/**
 * A sentence.
 */
export class Sentence {

    annotationTag = null

    /**
     * @param {*} sent_id the ID of the sentence.
     * @param {string} text the string of the sentence.
     */
    constructor(sent_id, text) {
        this.sent_id = sent_id
        this.text = text
    }
}

/**
 * The speech acts to annotate with, including 'unknown' and 'none' tags.
 */
const AnnotationTags = {
    assertion: 'assertion',
    question: 'question',
    directive: 'directive',
    expressive: 'expressive',
    hypothesis: 'hypothesis',
    unknown: 'unknown',
    none: 'none'
}

/**
 * Retreive the current date and time formatted as a string. It's on the format 
 * YYYY-MM-DD hh:mm:ss.
 * @returns the current date and time formatted as a string.
 */
function currentDateAndTime() {
    const currentDate = new Date()

    // Get date components
    const year = currentDate.getFullYear()
    const month = String(currentDate.getMonth() + 1).padStart(2, '0')
    const day = String(currentDate.getDate()).padStart(2, '0')

    // Get time components
    const hours = String(currentDate.getHours()).padStart(2, '0')
    const minutes = String(currentDate.getMinutes()).padStart(2, '0')
    const seconds = String(currentDate.getSeconds()).padStart(2, '0')

    // Construct the date and time string
    const dateTimeString = `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`

    return dateTimeString
}


class Session {

    // The number of sentences that has been annotated this session.
    progress = 0

    // Callback for when the current sentence has changed.
    onSentenceChanged = null

    // Callback for when the session is completed.
    onCompletion = null

    // The url for the file with the completed results.
    resultsURL = null
    
    /**
     * @param {string} session_id a unique ID of the current session.
     * @param {Array<Sentence>} sentences the sentences to annotate.
     */
    constructor(session_id, sentences) {
        this.session_id = session_id
        this.sentences = sentences
        this.startTime = currentDateAndTime()
    }

    /**
     * The current sentence to be annotated.
     */
    get currentSentence() {
        return this.sentences[this.progress]
    }

    /**
     * The number of sentences to annotate.
     */
    get sentenceCount() {
        return this.sentences.length
    }

    /**
     * Annotate the current sentence and move on to the next sentence.
     * @param {string} annotationTag the tag to annotate with.
     */
    annotate(annotationTag) {
        this.sentences[this.progress].annotationTag = annotationTag
        this.progress++

        // Complete the session if all sentences have been annotated.
        if (this.progress === this.sentences.length) {
            this.finishSession()
        }
        // Else notify UI about next sentence.
        else {
            this.fireOnSentenceChanged()
        }
    }

    /**
     * Undo the previous annotation and go back to that sentence.
     */
    undo() {
        if (this.progress === 0) {
            throw Error('Cannot undo because there is no previous sentence.')
        }
        this.progress--
        this.fireOnSentenceChanged()
    }

    /**
     * Notify callback that the current sentence has changed.
     */
    fireOnSentenceChanged() {
        if (this.onSentenceChanged !== null) {
            this.onSentenceChanged()
        }
    }

    /**
     * Finish the session and create a downloadable data file.
     */
    finishSession() {
        // Format data as lines of strings.
        const lines = []
        
        // Write the session data.
        lines.push('# session_id = ' + this.session_id + '\n')
        lines.push('# start_time = ' + this.startTime + '\n')
        lines.push('# end_time = ' + currentDateAndTime() + '\n')
        
        // Write all sentences as lines.
        for (let sentence of this.sentences) {
            lines.push('\n')
            if (sentence.sent_id !== null) {
                lines.push('# sent_id = ' + sentence.sent_id + '\n')
            }
            lines.push('# text = ' + sentence.text + '\n')
            lines.push('# speech_act = ' + sentence.annotationTag + '\n')
        }
        
        // Create blob of lines.
        const data = new Blob(lines, {type: 'text/plain'})
        this.resultsURL = window.URL.createObjectURL(data)

        // Do completion callback.
        if (this.onCompletion !== null) {
            this.onCompletion()
        }
    }
}

class View {
    
    $progressBar = document.querySelector('#annotated-sentences')
    $progressCount = document.querySelector('#progress-count')
    $sentence = document.querySelector('.sentence')
    $buttons = document.querySelector('.buttons')
    $undoButton = document.querySelector('#undo-button')

    /**
     * Create a new view for the given session.
     * @param {Session} session the session to display.
     */
    constructor(session) {
        this.session = session
        session.onSentenceChanged = () => {
            this.updateView()
            // Todo: freeze buttons.
        }
        this.updateView()
    }

    /**
     * Update the elements in the document with data from the session.
     */
    updateView() {
        this.$progressBar.value = this.session.progress
        this.$progressBar.max = this.session.sentenceCount
        this.$progressCount.textContent = `${this.session.progress}/${this.session.sentenceCount}`
        this.$sentence.textContent = this.session.currentSentence.text

        this.$undoButton.disabled = this.session.progress == 0
    }
}


class Controller {

    $buttons = document.querySelector('.buttons')
    $undoButton = document.querySelector('#undo-button')
    $endSessionButton = document.querySelector('#end-session-button')

    /**
     * Create a controller to send input and manipulate a session with.
     * @param {Session} session the session to send input to.
     */
    constructor(session) {
        this.session = session

        // Add click listeners to annotation buttons.
        document.querySelector('#button-assertion').addEventListener(
            'click', () => this.clickAnnotate(AnnotationTags.assertion))

        document.querySelector('#button-question').addEventListener(
            'click', () => this.clickAnnotate(AnnotationTags.question))

        document.querySelector('#button-directive').addEventListener(
            'click', () => this.clickAnnotate(AnnotationTags.directive))

        document.querySelector('#button-expressive').addEventListener(
            'click', () => this.clickAnnotate(AnnotationTags.expressive))

        document.querySelector('#button-unknown').addEventListener(
            'click', () => this.clickAnnotate(AnnotationTags.unknown))
        
        document.querySelector('#button-none').addEventListener(
            'click', () => this.clickAnnotate(AnnotationTags.none))

        // Add click listener to undo button.
        document.querySelector('#undo-button').addEventListener('click', () => session.undo())
    }

    /**
     * Click an annotation button and tell the session to annotate the current sentence.
     * @param {string} annotationTag 
     */
    clickAnnotate(annotationTag) {
        console.log('clickAnnotate: ', annotationTag)
        session.annotate(annotationTag)
    }
}


// Read sentences from a file.
const fileURL = `test sentences no IDs.💬` // Change this to load other file.
const sentences = await parseSentences(fileURL, -1)
sentences.sort(() => Math.random() - 0.5) // Shuffle sentences.
console.log('Number of sentences: ', sentences.length)

// Create new session.
const session = new Session(null, sentences)
const sessionName = fileURL.split('/').pop().split('.')[0]
session.session_id = `${sessionName}-${session.startTime}`
new View(session)
new Controller(session)

// Download data when session completes.
session.onCompletion = () => {
    console.log('session completed! Downloading data.')

    // Create download link.
    const downloadLink = document.createElement('a')
    downloadLink.setAttribute('download', `${session.session_id}.✏️`)
    downloadLink.href = session.resultsURL

    // Wait and then auto-click the link.
    window.requestAnimationFrame(() => {
        const mouseEvent = new MouseEvent('click')
        downloadLink.dispatchEvent(mouseEvent)
        downloadLink.remove()
    })
}