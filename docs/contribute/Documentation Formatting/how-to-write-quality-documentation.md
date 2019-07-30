---
title: Writing Quality Documentation
excerpt: Writing a guide or tutorial for GS Quant? Learn best practices for working with Markdown and our documentation format.
datePublished: 2019/05/29
githubUrl: https://github.com/goldmansachs
keywords:
  - Contribute
  - Markdown
  - Frontmatter
  - Documentation
  - Editorial
  - Content
  - Style guide
links:
  - title: Goldman Sachs
    url: https://gs.com/
authors:
  - name: Alizah Herman
    github: alizahgrace
---


## How to Write Quality Documentation for GS Quant
This is a brief editorial guide for writing developer documentation and technical content on developer.gs.com. These guidelines will help you to write in our voice and tone, and ensure consistency across language, grammar, and formatting. All Goldman Sachs Developer documentation is written in [Markdown](https://daringfireball.net/projects/markdown/) or [MDX](https://mdxjs.com/).


### Best Practices
- Be conversational and human — like you’re speaking with another person, not delivering a lecture. 
- Use simple sentences to make content easy to scan and digest.
- Read what you wrote out loud. If it feels awkward to say, it will be awkward to read. 
- Always check spelling and grammar before publishing. Pro tip: copy and paste into Microsoft Word to check.
<br/><br/>
___
## Voice and Tone
Be conversational, human, and friendly in your writing. Successful documentation will sound like it’s coming from a smart friend who understands what you’re trying to accomplish. 

### Things to Do
- **Start with why:** Focus on what developers are trying to accomplish and why. Use that understanding to structure your article according to those tasks and goals.<br/><br/>
-	**Use common language:** Aim for language developers would use. Avoid excess jargon for the sake of jargon’s sake, but don’t sacrifice technical integrity. Use examples to explain concepts and demonstrate how to maximize value. <br/><br/>
-	**Get to the point:** Everyone is strapped for time and on information overload. If a developer is reading your article, they’re actively trying to get something done. If there are steps that need to be taken first in order to do your tutorial, put those at the beginning of your article.  <br/><br/>
-	**Use chunks for quick processing:** Use short, simple sentences of 50-75 characters. Separate concepts into different paragraphs to create whitespace. The first and last sentences — closest to the whitespace — are the most memorable. Make use of h tags to create clear visual hierarchies. <br/><br/>
-	**Be empathetic:** Anticipate questions readers may have, and proactively provide answers. Communicate confidently, but not arrogantly. Be upfront and honest about situations that will be frustrating or require more work. Focus on what matters most. <br/><br/>
- **Use an active voice:** Aim for actionable language and an active voice. Lead with verbs, and avoid passive sentences. Speak to what value the reader can get, not what the article subject offers. 

### Things to avoid
- Buzzwords 
- Insensitive language 
    - <span style="color:#FA5343;">Incorrect:</span> *dummy* text
    - <span style="color:#03AB65;">Correct:</span> *placeholder* text
- Caveats or callouts within sentences
    - <span style="color:#FA5343;">Incorrect:</span> "Please note, ..."
    - <span style="color:#03AB65;">Correct:</span> Use blocks for callouts
- Sentence fragments
- Run-on sentences
- Exclamation marks
- Patronizing language
    - <span style="color:#FA5343;">Incorrect:</span> "Let's look at ... "
- Variants of "simply" (it's either unncessary or frustrating)
    - <span style="color:#FA5343;">Incorrect:</span> "It's that simple"
    - <span style="color:#FA5343;">Incorrect:</span> "Simply..."
- Internet slang and abbreviations 
- Passive headlines and sentences
    - <span style="color:#FA5343;">Incorrect:</span> The documentation for this API offers developers the ability to learn how to query datasets that are made available on GS Quant 
    - <span style="color:#03AB65;">Correct:</span> How to query datasets with GS Quant 

### Tips and tricks
- Read it out loud. If you're tripping over an awkward sentence, take a step back and think about what you're actually trying to communicate. How would you say it if you were telling a developer in person?
- Ask a colleague to read through your article before you hit publish. It never hurts to get an outside perspective. 
- Tone is important, but content is more important. Even if the tone sounds less human than you'd like, remember that the most important thing is to deliver the vaulable information developers need. 
<br/><br/>

___
## Grammar, punctuation, and formatting
All Goldman Sachs Developer documentation is written in [Markdown](https://daringfireball.net/projects/markdown/) or [MDX](https://mdxjs.com/). Avoid manually inserting `H1` headings. Goldman Sachs Developer automatically inserts and formats document titles [provided as metadata](/gsquant/contribute/Documentation-Formatting/adding-metadata).

### Abbreviations
- Use standard American abbreviations.
- Avoid internet abbreviations
    - <span style="color:#FA5343;">Incorrect:</span> tl;dr

### Branded names and terms
- GS Quant
    - <span style="color:#FA5343;">Incorrect:</span> gs quant, gs-quant, GS quant
    - <span style="color:#03AB65;">Correct:</span> GS Quant
- PlotTool
    - <span style="color:#FA5343;">Incorrect:</span> plottool, Plottool, plotTool
    - <span style="color:#03AB65;">Correct:</span> PlotTool
- Goldman Sachs Developer
    - <span style="color:#FA5343;">Incorrect:</span> gs developer, GS developer, Goldman Developer, Goldman Sachs Dev
    - <span style="color:#03AB65;">Correct:</span> Goldman Sachs Developer, GS Developer

### Capitalization
- Use sentence case for headlines and titles (only the first letter is capitalized).

### Contractions
- As a general rule, use contractions to maintain our human tone. 
    - <span style="color:#FA5343;">Incorrect:</span> they are, you will, it is
    - <span style="color:#03AB65;">Correct:</span> they're, you'll, it's

### Emphasis
- **Bold** OR *italics*, not both
- Use emphasis extremely sparingly — if everything is emphasized, nothing is emphasized. 

### Localization
- Content will be translated into other languages, so it's important to keep these tips in mind:
    - Run articles through spell check before publishing to ensure no spelling, grammatical, or punctuation errors.
    - Aim for short and simple sentence construction. 
    - Include all small prepositions, like "a", "the", and "is". 

### Numbers
- In general, spell out numbers 0-9 
- Use numerals for numbers above 10

### Punctuation
#### Periods
-  Only use a period on bullet points with full sentences. <br/>*Example:*
    - Things you should do:
      - Get to the point.
      - End sentences with periods.
- Don't use periods on bullet points without proper sentences. <br/>*Example:*
    - This list includes:
      - bullets
      - periods
      - punctuation
- Embrace the period to avoid run-on sentences. If you need more than 2 commas or a semi-colon, you can probably split it into two sentences.
#### Commas
- In a series of three or more items, use a comma before the final "and" and "or".
- In sentences containing two independent clauses, add a comma after the first clause.
#### Ellipses
- Don't use ellipses (...).
#### Exclamation points
- Don't use exclamation points (unless part of a code sample).
- Use blocks for callouts.
#### Slashes
-  Don't use slashes to separate alternative word options.
    - <span style="color:#FA5343;">Incorrect:</span> wrong/incorrect
    - <span style="color:#03AB65;">Correct:</span> wrong or incorrect

### Spelling and localization
- Use American English <br/> *Examples:*
    - <span style="color:#FA5343;">Incorrect:</span> localisation, colour
    - <span style="color:#03AB65;">Correct:</span> localization, color
