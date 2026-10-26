# Translator and Checker Brief

Thank you for helping with this project. We are studying whether AI chatbots behave less safely when people write to them in Telugu, Tamil or Hindi than in English. Your translations let us separate real language effects from problems caused by machine translation.

## ⚠️ Content warning

Many prompts in your sheet ask for **harmful things**: violence, hate speech, self-harm, fraud, sexual content, discrimination by caste, religion or gender, and more. They come from public research benchmarks and were written to test AI safety. Some may be upsetting.

- **You can skip any prompt, for any reason.** Put `y` in the `skip` column. You don't need to explain, and skipping will never count against you.
- Take breaks whenever you need them. There is no daily quota.
- If the material is affecting you, stop and tell Vinith. You can step back from any category or from the work entirely.

## 🚫 No AI or machine translation

For **human translations**, do not use Google Translate, ChatGPT, Claude, Gemini or any other AI or machine-translation tool, not even to get a first draft or check a word. Dictionaries are fine.

This is the core of the study: we compare human translation against machine translation, so a human translation that started from a machine draft would make the comparison meaningless.

For romanized and code-mixed sheets, you edit a draft we generated. That draft may come from a tool; your job is to make it correct and natural.

## Style guide

### Human translation (native script)

- **Translate the meaning, not word by word.** Write it the way a native speaker would naturally ask it.
- **Keep the intent and strength the same.** Don't soften a harmful request or make it more extreme. If the English is rude, the translation should be equally rude. If it's polite, keep it polite.
- **Keep the register.** Casual English becomes casual Telugu, Tamil or Hindi. Formal stays formal.
- **Names, numbers, places and technical terms:** keep them as they are, or use the form a native speaker would normally write.
- **English words that people normally use as-is** (e.g. "computer", "password") can stay in English if that's how people actually talk. Use the native word if that's more natural.
- **If something has no good equivalent,** translate as closely as you can and explain in `notes`.
- **Don't add anything:** no warnings, explanations or extra context.

### Romanized

The same text as the final human translation, written in Latin (English) letters.

- Romanization convention: `[TO BE FIXED together with the romanization tool]`
- Fix any wrong spellings in the draft. Keep it readable to a native speaker who types this way.

### Code-mixed

The same meaning, with words switched between your language and English within the sentence, the way people actually text or chat (Tenglish, Tanglish, Hinglish).

- Make it sound natural. Rewrite the draft freely if it reads oddly.
- Keep the same intent and strength as the English.
- Script: `[TO BE FIXED together with the code-mix drafting method]`

## Using the sheet

Open the CSV in Google Sheets or Excel. Only fill in these columns:

| Column | What to do |
|---|---|
| `final_text` | Your finished text |
| `skip` | `y` to skip this prompt |
| `notes` | Optional: anything we should know |

Don't change `version_id`, `source`, `source_id`, `harmful` or `harm_category`. `english_text` is the original prompt. `reference_text` and `draft` appear only in romanized and code-mixed sheets.

When you're done, or at any checkpoint, send the sheet back as CSV.

## Privacy

Don't put personal information (yours or anyone else's) in translations or notes. These prompts are sent to commercial AI services that may keep the data.

## Questions

Contact Vinith Ayapilla.
