# Synthetic-Multiple-Negative-Summary

<File Description>

- code
	- GPT3.5 turbo - Eval
		: LLM evaluation code

	- GPT3.5 turbo - highlights
		: LLM summarization code

	- prompt: Data aumgentation(varing-level negative data) prompt
  
	- result avg
		: Get average of LLM evaluation result

	- result sorting
		: Get sorted data by score

	- run_summarization
   		: BART fine-tuning

-  data
	- https://drive.google.com/drive/folders/1BycNzCiyVFT-bgdIYWQEwuFjKTx5m_tB?usp=drive_link
	- seed
		- CNNDM data source: https://huggingface.co/datasets/cnn_dailymail - (Subset 3.0.0)
		- train_10000
			: 10,000 sampled train data from original(Hugging Face) train data
			: {article, highlights, id}
	
		- test_500
			: 500 sampled test data from original(Hugging Face) test data
			: {article, highlights, id}

	- result_data
		- train_augmented_10000
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

- result
	- Summary_Eval
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

	- LLM_Eval
		- result_highlight_option1
			: 500 raws of {article, reference, pred_summary, coherency, consistency, fluency, relevance, model}

		- result_highlight_option2

		- result_highlight_option3

		- LLM_Eval results
			: Averaged score of LLM evaluation





