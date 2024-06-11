# CNNDM data source: https://huggingface.co/datasets/cnn_dailymail - (Subset 3.0.0)

<File Description>

- kcc prompt: Data aumgentation(varing-level negative data) prompt

- code
	- data sampling
		: Train/Test data sampling code from original(Hugging Face) data
	
	- KCC 2024_GPT3.5 turbo - Eval
		: LLM evaluation code

	- KCC 2024_GPT3.5 turbo - highlights
		: LLM summarization code

	- result avg
		: Get average of LLM evaluation result

	- result sorting
		: Get sorted data by score

- data
	- kcc_train_10000
		: 10,000 sampled train data from original(Hugging Face) train data
		: {article, highlights, id}

	- kcc test_500
		: 500 sampled test data from original(Hugging Face) test data
		: {article, highlights, id}

- results
	- kcc_train_augmented_10000
		: 10,000 sampled train data + 3 level hallucinated summary in each data
		: {article, highlights, id, llm_output, parsed_output{summary, hallucinated_summary_low, hallucinated_summary_mid, hallucinated_summary_high, explanation}, model}
	
	- highlight_train_dataset1
		: 9,820 parsed train data
		: {article, reference}

	- highlight_train_dataset2
		: 39,280 parsed train data -> [Hallucination!!]No[Article], [Hallucination!!]Yes[Article]
		: {article, reference}

	- highlight_train_dataset3
		: 39,280 parsed train data -> [Hallucination!!]No[Article], [Hallucination!!]Meduim[Article], [Hallucination!!]High[Article]
		: {article, reference}

	- highlight_test_dataset1
		: 500 parsed test data
		: {article, reference}

	- highlight_test_dataset2_3 ->  [hallucination!!]No[Article]
		: 500 parsed test data
		: {article, reference}

	- summary_output_highlight
		- option1
			- all_results
				: Rouge socre & Training Information
			- predictions
				: 500 raws of {article, reference, pred_summary}

		- option2
			- all_results
			- predictions

		- option3
			- all_results
			- predictions

	- llm_eval_output_highlight
		- result_highlight_option1
			: 500 raws of {article, reference, pred_summary, coherency, consistency, fluency, relevance, model}

		- result_highlight_option2

		- result_highlight_option3

		- LLM_Eval results
			: Averaged score of LLM evaluation





