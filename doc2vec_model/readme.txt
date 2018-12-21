doc2vec 		documentation 

################# Training part:	train_model.py #############################

parameters:		vector_size
				train_epoch
				...
variable: 		pretrained_emb: there is a pretrained_word_emeddings, which include some trained model. if input none to this variable, that means use without pretrained embeddings

#Step1:
				change the value of parameters according to the specific requirements 
				
#Step2:
				choose appropriate corpus for training. input to variable 'train_corpus'
				
#Step3:
				set output path to variable 'saved_path'
				
#Step4:
				all set. could start training 
				
				
################ vector generation part:	infer_test_v1.py ####################


#step1:
				choose the training model and assign it to variable 'model'

#step2:
				choose the input file that for vector generation
				variable 'input_file'
				
#step3:
				set output filename and path
				variable 'output'
				
#step4:
				all set. could start generating 
				
								