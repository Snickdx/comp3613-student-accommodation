COMP 3613 BITS&GIGGLES REQUIREMENTS INTERVIEW CHATS\

We interviewed stakeholders for the Job Board and Career Advising scenarios before choosing Student Accommodation. 
We chose it because our group members had worked in this domain before, also because the Campus Accommodation Admin 
gave clear rules for each stage of a listing, which gave us a very detailed special feature to design.
 The Job Board had a similar lifecycle but its administrator reported no major issues with it and 
 the Career Advising concerns were mostly about outdated data and the interface. 



Exploratory Interview 1: Job Board (job board administrator)
Who does what: the admin approves listings, employers move applications, students apply and watch their status.
Special feature rules: applications go submitted → reviewed → shortlisted, rejected, or hired, with no skipping and no undoing a rejection.
Issues: students get no updates after applying, and resubmitting rejected listings is slow for employers.


Hello, thank you for meeting with us. Can you tell us a bit about your role and what exactly the job board is mainly used for right now?
06:54 PM
vector:job-board:administrator
Hi there! Thanks for having me. So, my role as the Job Board Administrator is to manage the job board for our university. I review job listings submitted by employers, decide whether to publish or reject them, and make sure everything runs smoothly for our students.
Right now, the job board is mainly used to connect our eligible DCIT students with job opportunities. Employers post their job listings, and once I approve them, students can see and apply for those jobs. It's all about making it easier for our graduates to find work in their field.
06:54 PM2.0s
Okay, so you mentioned students apply once a listing is approved. After a student applies, what happens to that application from start to finish? Like what stages does it go through and who moves it along?
06:55 PM
vector:job-board:administrator
Once a student applies, their application goes through a few stages. First, it gets a status of "submitted." From there, the employer who posted the job can review the applications. They can change the status to "reviewed," "shortlisted," "rejected," or "hired" based on their evaluation.
As the administrator, I don’t change those statuses; that’s all up to the employer. I just make sure everything is set up correctly for them to manage their applications. Once the employer updates the status, the student can see their current application status on the platform. It’s pretty straightforward, but the employers have to keep track of everything after that initial application.
06:55 PM2.7s
Are there rules to the status change? eg should an employer be able to change the status from rejected back to shortlisted or skip straight from submitted to hired? Has there been any issues with status changes thus far?
06:57 PM
vector:job-board:administrator
Good question! Yes, there are rules for changing the statuses. An employer can only move an application from "submitted" to "reviewed," then to "shortlisted," "rejected," or "hired." They can't jump straight from "submitted" to "hired" or change a "rejected" application back to "shortlisted."
So far, we haven't had any major issues with status changes, but it's important for employers to follow that flow to keep things clear for the students. If they don't, it could create confusion for applicants who are waiting to hear back.
06:57 PM2.1s
Thanks, noted. lastly, if we could improve or fix some things on the job board what would be the most importaant to you and is there anything in the current system that is frustrating to you, employers or the students?
07:00 PM
vector:job-board:administrator
If I could improve something on the job board, the biggest thing would be to create a feedback loop for applicants. Right now, once students apply, they often don’t know if their application has been reviewed or what the next steps are. It would be great if we could provide them with more updates or notifications throughout the process.
As for frustrations, sometimes employers find the revision process for rejected listings a bit cumbersome. They have to revise and resubmit before I can review it again, and that can slow things down. For students, the lack of feedback after applying is definitely a common concern. Overall, making the communication clearer for everyone involved would really help.
07:00 PM2.8s
Controls
Shared interview budgetShared pool
11k left · 4.0k / 15k used27% used
Sized for one focused requirements interview. Usage updates after each reply.
Scenario
Job Board
Locked · job-board
PersonaJob Board AdministratorEmployerGraduate Applicant
Mode
Vector RAG▾

▾
Exploratory Interview 2: Career Advising


Who does what: students explore from a career or from their courses, and the advisor guides without pushing one outcome.
Special feature rules: both flows run the same steps from different ends, namely skills lookup, matching, ranking by overlap, then missing-course gaps. Nothing is enrolled or booked.
Issues: outdated skill mappings, a cluttered interface, and suggestions that don’t feel personal.
Hi thanks for meeting with us. Can you tell me a bit about your role and how this careeer advising system is used right now
07:14 PM
vector:career-advising:career_advisor
Sure! I’m a career advisor, and my main role is to help students connect their courses with potential career paths. Right now, we use this advising system to guide students in exploring their options. They can either start by picking a career they’re interested in or by entering the courses they’re taking. The system then suggests careers based on the skills and competencies linked to those courses.
It’s really about providing them with options and helping them see how their education aligns with different jobs, without pushing them toward a single outcome. We want to make sure they feel supported in exploring different paths, especially since many students aren’t sure what they want to do yet.
07:14 PM2.0s
Okay so students can start from a career or from their courses. can you walk me through what happens step by step in each case? So like what the system does in betwenn the student's input and the suggestions they see at the end?
07:23 PM
vector:career-advising:career_advisor
Absolutely! So, let’s break it down.
Career-First Flow: When a student starts by selecting a career, they might describe what they’re interested in or pick from a list. Once they input that, the system looks at the skills and competencies required for that career. Then, it matches those with the courses the student might need or that align well with that career path. Finally, it presents a list of suitable careers, showing how their chosen career connects to the courses they could take, but always in a way that emphasizes it’s just a suggestion, not a must-do.
Course-First Flow: If they start by entering the courses they’re currently taking or interested in, the system does something similar. It checks the skills and competencies linked to those courses and then finds careers that match those skills. Again, it presents a list of potential careers, ranked by how well they align with the courses the student has chosen, but it’s clear that these are just options.
In both cases, the system also identifies any missing courses they might need for their desired career path, but it stops there—no enrollment or booking steps involved. It’s all about giving them the information they need to make informed choices without feeling pressured.
07:23 PM4.2s
Okay so it sounds like they both go through similar steps but they just start from different ends. what are the rules, if any, on how those steps should work like how careers are ranked or what counts as a missing course? also has anything ever gone wrong such as the two flows giving results that dont make sense?
07:27 PM
vector:career-advising:career_advisor
You're right; both flows do follow a similar process but start from different points.
As for the rules, the ranking of careers is based on the overlap of skills and competencies between the student's courses and what's required for the careers they’re interested in. We want to ensure that the suggestions are relevant and make sense for the student’s current situation. The system ranks them in a transparent way, so students can see why certain careers are suggested over others.
When it comes to identifying missing courses, the system checks against the requirements for the career the student is interested in and highlights any gaps in their current course selections. It’s important that this identification is clear, so they know what they might need to pursue that career.
As for things going wrong, we’ve had a few instances where the suggestions felt a bit off, usually due to outdated skill mappings or if a student entered courses that didn’t align well with any career options. We’re constantly working to refine the system and improve the accuracy of those connections. It’s a learning process, and feedback from students helps us make it better!
07:27 PM3.4s
Thank you for that. Last thing if we could improve or fix a few things on the advising system what would matter the most to you? is there anything currently that frustrates users?
07:29 PM
vector:career-advising:career_advisor
Great question! If we could improve a few things, I'd say the biggest focus should be on ensuring the skill mappings are always up-to-date and accurate. Sometimes, we find that certain careers or courses don’t reflect the latest industry trends, which can lead to confusion for students.
Another area for improvement would be the user interface. Making it more intuitive could really help students navigate their options more easily. Sometimes, they get overwhelmed with information, so simplifying how we present the suggestions could make a big difference.
As for frustrations, students occasionally feel like the recommendations don’t fully capture their interests or unique situations. They want to see more personalized options based on their specific courses or career aspirations. So, enhancing the system’s ability to tailor suggestions would definitely help improve their experience.
07:29 PM2.9s
Controls
Shared interview budgetShared pool
11k left · 4.0k / 15k used27% used
Sized for one focused requirements interview. Usage updates after each reply.
Scenario
Career Based Advising
Locked · career-advising
PersonaCareer Advisor
Mode
Vector RAG▾

