from datasets import load_dataset
from datasets import load_metric
from sentence_separator import SentenceSeparator
from summarizer_model import SummarizerModel
import time


def test_system( dataset_name="cnn_dailymail"):
    # define model
    summarizer = SummarizerModel()
    # define sentence separator
    sent_sep = SentenceSeparator()
    # load metric
    metric = load_metric('rouge', seed=12345)

    # load dataset
    if dataset_name=="cnn_dailymail":
        dataset = load_dataset('cnn_dailymail', '3.0.0', split="test")
        
    elif dataset_name=="newsroom":
        dataset = load_dataset('newsroom', data_dir="C:\\Users\\krist\\Desktop\\Newsroom", split="test")
        dataset = dataset.filter(lambda test_case: test_case['density_bin'] == 'extractive')
    
    # print dataset length
    dataset_length = len(dataset)
    print(" ------------- DATASET LENGTH -------------------")
    print("  "+ str(dataset_length) + " records")
    print(" ------------- TESTING ... -------------------")

    start_time = time.time()

    if dataset_name=="cnn_dailymail":
        # test model on dataset CNN / DAILY MAIL
        for num,test_case in enumerate(dataset):
            # extract text and summary
            text = test_case["article"]
            gold_summary = test_case["highlights"]
            # create a summary using the model
            numOfSents = len(sent_sep(gold_summary, min_length=20))
            model_summary = summarizer(text, num_sentences=numOfSents, min_length=40, use_first_sent=False)
            # add the prediction to the memory
            metric.add(prediction=model_summary, reference=gold_summary)
            if ( (num + 1) % 100) == 0:
                checkpoint = time.time()
                time_for_one = (checkpoint-start_time)/(num+1)
                estimated_seconds = time_for_one*(dataset_length-(num+1))
                estimated_hours = estimated_seconds/3600
                estimated_hours = round(estimated_hours, 2)
                print("--- TEST CASE: " + str(num+1) + " ---- ESTIMATED TIME: " + str(int(estimated_seconds))+ "s, "+ str(int(estimated_hours))+ "h "+str(int((estimated_hours % 1)*60))+ "min")
    
    elif dataset_name=="newsroom":
        # test model on dataset NEWSROOM
        for num,test_case in enumerate(dataset):
            # extract text and summary
            text = test_case["text"]
            gold_summary = test_case["summary"]
            # create a summary using the model
            numOfSents = len(sent_sep(gold_summary, min_length=20))
            model_summary = summarizer(text, num_sentences=numOfSents, min_length=40, use_first_sent=False)
            # add the prediction to the memory
            metric.add(prediction=model_summary, reference=gold_summary)
            if num == 9999:
                break
            if ( (num + 1) % 100) == 0:
                checkpoint = time.time()
                time_for_one = (checkpoint-start_time)/(num+1)
                estimated_seconds = time_for_one*(9999-num)
                estimated_hours = estimated_seconds/3600
                print("--- TEST CASE: " + str(num+1) + " ---- ESTIMATED TIME: " + str(int(estimated_seconds))+ "s, "+ str(int(estimated_hours))+ "h "+str(int((estimated_hours % 1)*60))+ "min")
    
    end_time = time.time()

    print(" ------------- TESTING DONE! -------------------")
    # print elapsed time
    testing_time = end_time - start_time
    testing_time_hrs = testing_time/3600
    print(" -> Elapsed time : "+ str(int(testing_time)) + "s, " + str(int(testing_time_hrs))+ "h "+str(int((testing_time_hrs % 1)*60))+ "min")
    # compute the scores
    score = metric.compute()
    print(" ------------- MODEL PERFORMANCE -------------------")
    print(" -> ROUGE-1 : "+ str(score["rouge1"]))
    print(" -> ROUGE-2 : "+ str(score["rouge2"]))
    print(" -> ROUGE-L : "+ str(score["rougeL"]))
    print(" -> ROUGE-L(sum) : "+ str(score["rougeLsum"]))


if __name__ == "__main__":
    test_datasets=["cnn_dailymail", "newsroom"]

    test_system(test_datasets[1])
