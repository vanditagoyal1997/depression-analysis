# depression-analysis
## Objective 
To examine the feasibility of and aim to use different behavioral indicators for depression, consisting of, but not limited to, visual and audio features to design an effective testing model which can be made more accessible than traditional testing methods. 

## Dataset used
The database that we used for the training is a section of a bigger corpus, the “Distress Analysis Interview Corpus (DAIC)” (Gratch et al., 2014), that comprises of clinical interviews that were created to assist in the detection and the diagnosis of various psychological distress conditions like anxiety, depression, and PTSD.  The Data accumulated includes some audio and video recordings and comprehensive answers to a questionnaire. The interviews were taken by an animated virtual interviewer named Ellie, who was being controlled by a human interviewer from a different room. Data was then deciphered and interpreted for a number of verbal and nonverbal features. 

https://dcapswoz.ict.usc.edu/


## Application created
An end to end application was created using Flask to create a server and HTML, CSS and JS to create the user interface. To minimise human intervention in the process, a chatbot called DINA was created using ChatterBot to interact with the user and collect data (audio and video file)

Used OpenFace toolkit created by Tadas Baltrušaitis in collaboration with CMU MultiComp Lab led by Prof. Louis-Philippe Morency to analyse and extract Action Units data and Gaze data from video.
https://github.com/TadasBaltrusaitis/OpenFace

## Future Plan
1. Fix inputs to models in application
2. Diversify training dataset
3. Make models more robust and finding a better method to combine results
4. Using previous records of a user for prediction over a period of time and exploring relevant weightages for the same 
5. Implementation of better security features to ensure user privacy 




