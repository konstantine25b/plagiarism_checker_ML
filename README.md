# plagiarism_checker_ML

# PROJECT DESCRIPTION:

ENGLISH:
Final Project: Code Plagiarism Checker System
Objective: In this project, you will create a demo system for detecting code plagiarism. Your task is to build a system that can find similar code snippets from existing code repositories based on the code snippet provided by the user and determine whether the presented code is plagiarized.

Main Stages of the Project:

Fetching Code Repositories:
You need to gather a list of code repositories. For this, you can use the GitHub API or simply specify the links to the repositories in a configuration file.
The repositories you fetch should be cloned to your local environment using git clone.
Our recommendation is to choose 2-3 simple repositories for the system as we are building a simple system.

Code Indexing:
From the downloaded repositories, you should search for code files (for example, .py, .java, .c, etc.).
For each code file, you need to calculate a vector representation (embedding). For this, you should select an appropriate embedding model from the Hugging Face library. Ideally, find a model that works well for representing the semantic content of code.
The generated embeddings should be stored in a vector database. You can use libraries such as Faiss, ChromaDB, Pinecone, or another option you prefer.

Building the Plagiarism Checking System (RAG Principle):
You need to create an API (for example, using FastAPI) that will receive the content of a code file uploaded by the user (not the file itself, but its content as a string).
When the user submits a code snippet, your system must first search for similar code files in the vector database. For this, you will use the embedding of the provided code snippet and the vector database search function.
Next, you should connect to the LLMs (Large Language Models) through your preferred API. You should send the entire aggregated prompt to the LLM, including the code snippet provided by the user and the similar code files returned from the vector database (as context).
Importantly: The LLM should return only two words: "Yes" (if the code is plagiarized) or "No" (if the code is not plagiarized). To achieve this, you must use prompt engineering techniques. Also, ask the LLM to refer to the code files returned from the vector database as references (if plagiarism is confirmed).

System Evaluation:
You need to create a small dataset containing both plagiarized and non-plagiarized cases. You can create this manually or with the help of AI.
Using the created dataset, you should compare the results of the following three approaches:

Only RAG: Use your built RAG system and some threshold value for similarity to determine if the code is plagiarized.
Only LLM: Directly query the LLM with the user's code snippet and ask it to assess whether it's plagiarized.
Your Complete System: Use the fully functional system that combines vector search and LLM with reference-based answers.
The evaluation results should be saved in a CSV file.
Important Notes (This is a Demo System):

Note that this project primarily demonstrates the concept of plagiarism checking and not an ideal, fully-optimized system.
Indexing a large number of GitHub repositories requires significant computational resources (calculating embeddings) and time. There are also technical difficulties related to processing large code files. You may need to devise tricks to handle comparing large code files. For simplicity, select a few repositories with smaller code files.
Also, bear in mind that in an ideal case, plagiarism checking should be done between repositories rather than individual code files. However, for the simplicity of the project, we will limit the comparison to code files (as text files).
Requirements:

Indexing Script: You must write a separate Python script that will download the repositories and index the code files into the vector database. This script should be containerized using Docker.
Embedding Server: The embedding model should be hosted as a separate service. This service should also be containerized using Docker.
Plagiarism Checking API: The API responsible for checking plagiarism should be built using FastAPI. This API will accept an HTTP POST request with the content of the code file (as a string). The API should return a boolean variable indicating whether the code is plagiarized. This API should also be containerized using Docker.
Evaluation Script: You should write a script that runs the evaluation process and compares the results of the three approaches. This script should also be containerized.
Project Presentation:
After completing the project, you will individually present your work. We will not accept projects in ZIP file format. You should upload your project code to GitHub in your personal repository. The repository should be public (not public during the development process to avoid plagiarism ;) Your own code will be tested for plagiarism on each other). When presenting, you must provide the link to your repository. Your repository should contain a well-described README.md file in English, detailing the project structure, instructions for running it, and other important information. During the presentation, you will demonstrate your system, explain how you set it up, the technologies you used, the challenges you faced, and how you solved them. You should also show your code and answer any questions we have.

Deadlines and Support:
You will have 3 weeks to complete this project. During this time, you can reach out with any questions that will help you successfully complete the project.

Evaluation:
Please note that partial completion of the project will also be evaluated. So, don’t be discouraged by the complexity of the project, and try to do your best, even if you cannot complete every part of the task.

Additional Recommendations:

Start the project early to ensure you have enough time to complete all the stages.
Break the project into smaller, manageable sub-tasks.
Use Git from the beginning; don’t upload everything in one commit at the end.
Document your code and the project architecture.
Don’t hesitate to ask questions if something is unclear.

GEO:

ფინალური პროექტი: კოდის პლაგიარიზმის შემმოწმებელი სისტემა
მიზანი: ამ პროექტის ფარგლებში თქვენ შექმნით კოდის პლაგიარიზმის დემო სისტემას. თქვენი ამოცანაა ააწყოთ სისტემა, რომელიც შეძლებს მომხმარებლის მიერ მოწოდებული კოდის ნაწყვეტის მსგავსი კოდის მოძიებას არსებულ კოდის რეპოზიტორიებში და დაადგენს, არის თუ არა წარმოდგენილი კოდი პლაგიატი.
პროექტის ძირითადი ეტაპები:კოდის რეპოზიტორიების მოპოვება:
თქვენ უნდა მოიპოვოთ კოდის რეპოზიტორიების ჩამონათვალი. ამისათვის შეგიძლიათ გამოიყენოთ GitHub API ან უბრალოდ კონფიგურაციის ფაილში მიუთითოთ რეპოზიტორიების ლინკები.
მოპოვებული რეპოზიტორიები უნდა გადმოწეროთ თქვენს ლოკალურ გარემოში git clone-ის გამოყენებით.
ჩვენი რჩევაა რადგან მარტივ სისტემას ვაწყობთ აიღოთ მარტივი  2-3 რეპოზიტორია.
კოდის ინდექსირება:
გადმოწერილი რეპოზიტორიებიდან უნდა მოიძიოთ კოდის ფაილები (მაგალითად, .py, .java, .c და ა.შ.).
თითოეული კოდის ფაილისთვის უნდა გამოთვალოთ ვექტორული წარმოდგენა (ემბედინგი). ამისათვის თქვენ უნდა შეარჩიოთ შესაბამისი ემბედინგ მოდელი Hugging Face-ის ბიბლიოთეკაში. სასურველია იპოვოთ მოდელი, რომელიც კარგად მუშაობს კოდის სემანტიკური შინაარსის წარმოსადგენად.
მიღებული ემბედინგები უნდა შეინახოთ ვექტორულ მონაცემთა ბაზაში. შეგიძლიათ გამოიყენოთ ისეთი ბიბლიოთეკები, როგორიცაა faiss, chromadb, pinecone ან სხვა თქვენთვის სასურველი ვარიანტი.
პლაგიარიზმის შემოწმების სისტემის აწყობა (RAG პრინციპი):
თქვენ უნდა შექმნათ API (მაგალითად, FastAPI-ის გამოყენებით), რომელიც მიიღებს მომხმარებლის მიერ ატვირთული კოდის ფაილის კონტენტს (არა თვითონ ფაილს, არამედ მის შიგთავსს, როგორც სტრინგს).
როდესაც მომხმარებელი გამოაგზავნის კოდის ნაწყვეტს, თქვენმა სისტემამ ჯერ ვექტორულ მონაცემთა ბაზაში უნდა მოძებნოს მსგავსი კოდის ფაილები. ამისათვის გამოიყენებთ მოწოდებული კოდის ნაწყვეტის ემბედინგს და ვექტორული ბაზის ძიების ფუნქციას.
შემდეგ, თქვენ უნდა დაუკავშირდეთ LLM-ებს თქვენთვის სასურველი API-ის საშუალებით. თქვენ უნდა გადასცეთ მთლიანი აგრეგირებული პრომპტი LLM-ს მომხმარებლის მიერ მოწოდებული კოდის ნაწყვეტით და ვექტორული ბაზიდან დაბრუნებული მსგავსი კოდის ფაილებით (როგორც კონტექსტი).
მნიშვნელოვანია: LLM-მა პასუხად უნდა დააბრუნოს მხოლოდ და მხოლოდ ორი სიტყვა: "კი" (თუ კოდი პლაგიატია) ან "არა" (თუ კოდი არ არის პლაგიატი). ამის მისაღწევად თქვენ უნდა გამოიყენოთ პრომპტ ინჟინერიის ტექნიკები. ასევე, სთხოვეთ LLM-ს მიუთითოს ვექტორული ბაზიდან დაბრუნებული კოდის ფაილები, როგორც რეფერენსები (თუ პლაგიატი დადასტურდა).
სისტემის ევალუაცია:
თქვენ უნდა შექმნათ მცირე ზომის მონაცემთა ნაკრები, რომელიც შეიცავს პლაგიატისა და არაპლაგიატის შემთხვევებს. ეს შეგიძლიათ გააკეთოთ ხელით ან ხელოვნური ინტელექტის დახმარებით.
შექმნილი მონაცემთა ნაკრების გამოყენებით, თქვენ უნდა შეადაროთ შემდეგი სამი მიდგომის შედეგები:
მხოლოდ RAG: გამოიყენეთ თქვენი აწყობილი RAG სისტემა და რაიმე ზღვრული მნიშვნელობა (threshold) მსგავსების დასადგენად, რათა გადაწყვიტოთ არის თუ არა კოდი პლაგიატი.
მხოლოდ LLM: პირდაპირ მიმართეთ LLM-ს მომხმარებლის მიერ მოწოდებული კოდის ნაწყვეტით და სთხოვეთ შეაფასოს არის თუ არა ის პლაგიატი.
თქვენი აწყობილი სისტემა: გამოიყენეთ სრულად ფუნქციონალური სისტემა, რომელიც იყენებს ვექტორულ ძიებას და LLM-ს რეფერენსებით პასუხის გასაცემად.
ევალუაციის შედეგები უნდა შეინახოთ csv ფაილად.
მნიშვნელოვანი შენიშვნები (ეს არის დემო სისტემა):
გაითვალისწინეთ, რომ ეს პროექტი უფრო მეტად წარმოადგენს პლაგიარიზმის შემოწმების კონცეფციის დემონსტრაციას და არა იდეალურ, სრულყოფილ სისტემას.
დიდი რაოდენობით GitHub რეპოზიტორიების ინდექსირება მოითხოვს მნიშვნელოვან გამოთვლით რესურსებს (ემბედინგების გამოთვლა) და დროს. ასევე არსებობს ტექნიკური სირთულეები, რომლებიც დაკავშირებულია დიდი ზომის კოდის ფაილების დამუშავებასთან. შესაძლოა, თქვენ მოგიწიოთ რაიმე ხრიკის მოფიქრება, რათა შეძლოთ დიდი კოდის ფაილების შედარება. ამიტომაც აარჩიეთ მარტივი და ცოტა რაოდენობის რეპოზიტორიები.
ასევე გასააზრებელია რომ იდეალურ შემთხვევაში, პლაგიარიზმის შემოწმება უნდა მოხდეს რეპოზიტორიებს შორის და არა ცალკეულ კოდის ფაილებს შორის. თუმცა, პროექტის სიმარტივისთვის, ჩვენ შემოვიფარგლებით კოდის ფაილების (როგორც ტექსტური ფაილების) შედარებით.
მოთხოვნები:
ინდექსირების სკრიპტი: უნდა დაწეროთ ცალკე Python სკრიპტი, რომელიც შეასრულებს რეპოზიტორიების გადმოწერას და კოდის ფაილების ინდექსირებას ვექტორულ მონაცემთა ბაზაში. ეს სკრიპტი უნდა იყოს კონტეინერიზებული Docker-ის გამოყენებით.
ემბედინგ სერვერი: ემბედინგ მოდელი უნდა იყოს დაჰოსტილი, როგორც ცალკე სერვისი. ეს სერვისიც უნდა იყოს კონტეინერიზებული Docker-ის გამოყენებით.
პლაგიარიზმის შემოწმების API: პასუხისმგებელი API უნდა იყოს აწყობილი FastAPI-ის გამოყენებით. ეს API მიიღებს HTTP POST მოთხოვნას, რომლის body პარამეტრიც იქნება კოდის ფაილის კონტენტი (სტრინგის სახით). API-მ უნდა დააბრუნოს boolean ცვლადი, რომელიც მიუთითებს არის თუ არა კოდი პლაგიატი.  ეს API ასევე უნდა იყოს კონტეინერიზებული Docker-ის გამოყენებით.
ევალუაციის სკრიპტი: უნდა დაწეროთ სკრიპტი, რომელიც გაუშვებს ევალუაციის პროცესს და შეადარებს სამივე მიდგომის შედეგებს ასევე დოკერიზებული.
პროექტის წარდგენა:
პროექტის დასრულების შემდეგ, თქვენ ინდივიდუალურად წარადგენთ თქვენს ნამუშევარს. ჩვენ არ მივიღებთ პროექტებს ZIP ფაილის სახით. თქვენ უნდა ატვირთოთ თქვენი პროექტის კოდი GitHub-ის თქვენს პირად რეპოზიტორიაში. რეპოზიტორია უნდა იყოს საჯარო(დეველოპმენტის პროცესში არ უნდა იყოს საჯარო რადგან თვიდან ავიცილოთ პლაგიატი ;) თქვენივე კოდი იქნება გაშვებული ერთმანეთის პლაგიატზე 😀(ვხუმრობთ!)) ან ხელმისაწვდომი ჩვენთვის. წარდგენისას თქვენ უნდა მოგვაწოდოთ ამ რეპოზიტორიის ლინკი. რეპოზიტორიაში უნდა გქონდეთ კარგად აღწერილი README.md ფაილი ინგლისურ ენაზე, სადაც დეტალურად იქნება ახსნილი პროექტის სტრუქტურა, გაშვების ინსტრუქციები და სხვა მნიშვნელოვანი ინფორმაცია. წარდგენის დროს თქვენ ასევე ჩაგვიტარებთ თქვენი სისტემის დემონსტრაციას, მოგვიყვებით, თუ როგორ ააწყვეთ სისტემა, რა ტექნოლოგიები გამოიყენეთ, რა სირთულეებს შეხვდით და როგორ გადაჭერით ისინი. ასევე უნდა გვაჩვენოთ თქვენი კოდი და უპასუხოთ ჩვენს კითხვებს.
ვადები და მხარდაჭერა:
ამ პროექტის დასასრულებლად თქვენ გექნებათ 3 კვირა. ამ დროის განმავლობაში შეგიძლიათ მოგვმართოთ ნებისმიერი სახის კითხვით, რომელიც დაგეხმარებათ პროექტის წარმატებით შესრულებაში.
შეფასება:
გაითვალისწინეთ, რომ პროექტის ნაწილობრივი შესრულებაც შეფასდება. ამიტომაც, ნუ შეშინდებით პროექტის სირთულით და შეეცადეთ მაქსიმალურად კარგად შეასრულოთ დავალების ის ნაწილიც კი, რომლის სრულად დასრულებასაც ვერ მოახერხებთ.
დამატებითი რეკომენდაციები:
დაიწყეთ პროექტი ადრე, რათა საკმარისი დრო გქონდეთ ყველა ეტაპის დასასრულებლად.
დაყავით პროექტი მცირე, მართვად ქვედავალებებად.
გამოიყენეთ Git თავიდანვე, მხოლოდ 1 კომიტად არ ატვირთოთ ყველაფერი ბოლოს.
დოკუმენტირება გაუკეთეთ თქვენს კოდს და პროექტის არქიტექტურას.
ნუ მოგერიდებათ კითხვების დასმა, თუ რაიმე გაუგებარია.
წარმატებებს გისურვებთ თქვენს ფინალურ პროექტზე!