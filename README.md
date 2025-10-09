This is my repo for the Azure Cloud Resume Challenge (https://cloudresumechallenge.dev/).

<img width="1194" height="163" alt="Architecure Diagram" src="https://github.com/user-attachments/assets/8caf353d-3633-4979-8d75-cf778cfe39bd" />

<img width="1427" height="259" alt="image" src="https://github.com/user-attachments/assets/f3bbcd75-4772-4ca7-bd6d-6151537fd7f0" />


I’m not exactly sure how I came across https://cloudresumechallenge.dev/
, but it was love at first sight 😊 — and I decided to give it a go.

I chose Azure because I already had the required Az-900 certification and some hands-on experience. Every company I’ve worked for has used Azure in one way or another.

I also purchased the accompanying Cloud Resume Challenge book, which turned out to be a diamond in the rough — absolutely worth every penny. If you’re thinking about taking on this challenge, get the book!

Certification
“Your resume needs to have the AZ-900 certification on it This was an easy task as I had already had it”

This one was a breeze for me since I already had the AZ-900 under my belt.

HTML
“Your resume needs to be written in HTML.”

This was another straightforward step. There isn’t much to add here — but if you’re new to front-end development, I highly recommend freeCodeCamp and The Odin Project.
Both are excellent resources to get started with HTML, CSS, and JavaScript.

CSS
“Your resume needs to be styled with CSS. No worries if you're not a designer -- neither am I. It doesn't have to be fancy. But we need to see something other than raw HTML when we open the webpage.”

If it were up to me, the internet would still be running on HTML like it did in the early ’90s! I’m not an arty-farty type — design isn’t my strong suit. Still, I was happy to create a responsive layout that renders nicely on both desktop and mobile screens.

Static Website
“Your HTML resume should be deployed online as an Azure Storage static website. Services like Netlify and GitHub Pages are great and I would normally recommend them for personal static site deployments, but they make things a little too abstract for our purposes here. Use Azure Storage.”

HTTPS
“The Azure Storage website URL should use HTTPS for security. You will need to use Azure CDN to help with this.”

DNS
“Point a custom DNS domain name to the Azure CDN endpoint, so your resume can be accessed at something like my-c00l-resume-website.com. You can use Azure DNS or any other DNS provider for this. A domain name usually costs about ten bucks to register.”

Steps 4 to 6 need an update, in my opinion, since Azure CDN is being deprecated and is no longer offered.
Reference:

“Azure CDN Standard from Microsoft (classic) will be retired on September 30, 2027. To avoid any service disruption, it's important that you migrate your Azure CDN Standard from Microsoft (classic) profiles to Azure Front Door Standard or Premium tier by September 30, 2027. For more information, see Azure CDN Standard from Microsoft (classic) retirement.
Azure CDN from Edgio was retired on January 15, 2025. For more information, see Azure CDN from Edgio retirement FAQ.”

The current alternative is Azure Front Door, though it can be costly. I set it up just to test the process — it worked just as smoothly as Azure Static Web Apps (SWA) — and then deleted it.

Having experience with IIS and certificates, I wasn’t too worried about SWA’s built-in HTTPS support (which is a huge convenience).

In my opinion, Azure Static Web Apps (SWA) is much more affordable than Azure Front Door + Storage combo. SWA includes:

A free tier for hobby projects
A global CDN
And built-in HTTPS
Front Door is great for enterprise-scale needs (custom routing, WAF rules, advanced caching), but for simple static sites, SWA is the clear winner.

By the way, I purchased my custom domain through Cloudflare, and I highly recommend it for this project.

JavaScript
“Your resume webpage should include a visitor counter that displays how many people have accessed the site. You will need to write a bit of Javascript to make this happen. Here is a helpful tutorial to get you started in the right direction.”

I’m comfortable with JavaScript, but for the visitor counter, I used someone’s existing code as a starting point — a clean and simple algorithm that fit perfectly.

If you haven’t read Eloquent JavaScript
, go check it out. It’s one of my all-time favourite programming books — hands down.

Database
“The visitor counter will need to retrieve and update its count in a database somewhere. I suggest you use the Table API of Azure's CosmosDB for this. (Use serverless capacity mode for the database and you'll pay essentially nothing, unless you store or retrieve much more data than this project requires.)”

I handled this part quite easily, thanks to my background with MS SQL Server and other non-relational databases. Setting up Cosmos DB through the Azure Portal only took a few clicks, and it worked seamlessly.

API
“Do not communicate directly with CosmosDB from your Javascript code. Instead, you will need to create an API that accepts requests from your web app and communicates with the database. I suggest using Azure Functions with an HTTP trigger for this. They will be free or close to free for what we are doing.”

Python
“You will need to write a bit of code in the Azure Function; you could use more Javascript, but it would be better for our purposes to explore Python -- a common language used in back-end programs and scripts -- and its Azure SDK. Here is a good, free Python tutorial.”

Steps 9 and 10 gave me a few headaches. I spent quite a bit of time going through the official Azure Functions documentation.

I wrote the Python script with logic for v2, but it didn’t work as expected. I rewrote it for v1, but after a few days of troubleshooting, I discovered the real issue — a Python version compatibility problem.

After downgrading to Python 3.11, everything worked perfectly with v2. It was a good reminder that even small version mismatches can cause big headaches.

Tests
“You should also include some tests for your Python code. Here are some resources on writing good Python tests.”

I used Cypress for smoke testing, as recommended in the book (it uses JavaScript). I might later reimplement this using Python’s built-in unittest framework for consistency.

Infrastructure as Code
“You should not be configuring your API resources -- the Azure Function, the CosmosDB -- manually, by clicking around in the Azure console. Instead, define them in an Azure Resource Manager (ARM) template on a Consumption plan. This is called "infrastructure as code" or IaC. It saves you time in the long run.”

I’m currently preparing for the KCNA exam, and this step was incredibly helpful for gaining hands-on familiarity with Terraform.

Source Control
“You do not want to be updating either your back-end API or your front-end website by making calls from your laptop, though. You want them to update automatically whenever you make a change to the code. (This is called continuous integration and deployment, or CI/CD.) Create a GitHub repository for your backend code.”

CI/CD (Back End)
“Set up GitHub Actions such that when you push an update to your ARM template or Python code, your Python tests get run. If the tests pass, the ARM application should get packaged and deployed to Azure.”

CI/CD (Front End)
“Create a second GitHub repository for your website code. Create GitHub Actions such that when you push new website code, the Azure Storage blob automatically gets updated. (You may need to purge your Azure CDN endpoint in the code as well.) Important note: DO NOT commit Azure credentials to source control! Bad hats will find them and use them against you!”

I ended up with a very simple CI/CD pipeline and infrastructure setup — but it taught me a lot.

Here is my website: (https://zoltanolasz.com)

I’m currently exploring cloud roles, but most companies I’ve applied to use AWS. So, I plan to replicate this project in AWS soon to get a feel for the differences and broaden my skill set.

Blog Post
“Finally, in the text of your resume, you should link a short blog post describing some things you learned while working on this project. Dev.to or Hashnode are great places to publish if you don't have your own blog.”

And here we are — the final step! Writing this blog post has been a great way to reflect on everything I learned along the way. The challenge pushed me to explore both front-end and back-end technologies, DevOps practices, and cloud automation — all in one cohesive project.

If you’re considering it — do it. The Azure Cloud Resume Challenge is an incredible way to build real, demonstrable cloud skills while having fun along the journey. 🚀
