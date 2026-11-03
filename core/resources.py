"""
core/resources.py
Curated educational resources dynamically recommended based on student subject performance.
"""

SUBJECT_RESOURCES = {
    "Java": {
        "Needs Improvement": [
            {
                "title": "Java Programming for Beginners (freeCodeCamp)",
                "type": "Video Course",
                "url": "https://www.youtube.com/watch?v=A74TOX803D0",
                "desc": "Complete crash course covering variables, control flow, methods, and core OOP fundamentals.",
            },
            {
                "title": "W3Schools Java Interactive Tutorial",
                "type": "Interactive Guide",
                "url": "https://www.w3schools.com/java/",
                "desc": "Step-by-step interactive exercises with in-browser code runner.",
            },
        ],
        "Average": [
            {
                "title": "GeeksforGeeks Java Collections & OOP",
                "type": "Documentation",
                "url": "https://www.geeksforgeeks.org/java/",
                "desc": "Detailed guide on ArrayList, HashMap, Exception Handling, and Interfaces.",
            },
            {
                "title": "HackerRank Java Domain Practice",
                "type": "Coding Practice",
                "url": "https://www.hackerrank.com/domains/java",
                "desc": "60+ progressive problem-solving challenges to reinforce syntax and logic.",
            },
        ],
        "Good": [
            {
                "title": "Java Design Patterns & Architecture",
                "type": "Advanced Guide",
                "url": "https://refactoring.guru/design-patterns/java",
                "desc": "Master Factory, Singleton, Observer patterns and clean code principles.",
            },
            {
                "title": "Spring Boot Quickstart & REST APIs",
                "type": "Project Tutorial",
                "url": "https://spring.io/guides/gs/rest-service/",
                "desc": "Build scalable web backends with Spring Boot and Hibernate.",
            },
        ],
    },
    "Operating System": {
        "Needs Improvement": [
            {
                "title": "Operating Systems in 1 Hour - Gate Smashers",
                "type": "Video Lecture",
                "url": "https://www.youtube.com/playlist?list=PLxCzCOWd7aiGz9donHRrE9I3Mwn6XdP8p",
                "desc": "Crystal-clear conceptual explanations of Process Scheduling, Deadlocks, and Threads.",
            },
            {
                "title": "OS Fundamentals - Tutorialspoint",
                "type": "Notes & Cheatsheet",
                "url": "https://www.tutorialspoint.com/operating_system/index.htm",
                "desc": "Concise summary notes for quick revision of CPU scheduling, semaphores, and paging.",
            },
        ],
        "Average": [
            {
                "title": "Virtual Memory, Paging & Segmentation Explained",
                "type": "Reading Guide",
                "url": "https://www.geeksforgeeks.org/operating-systems/",
                "desc": "Comprehensive problem breakdowns with numerical examples of memory management.",
            },
            {
                "title": "OS Gate / Semester MCQ & Numerical Bank",
                "type": "Exam Practice",
                "url": "https://www.sanfoundry.com/1000-operating-system-questions-answers/",
                "desc": "Top 1000 standard exam questions with detailed explanations.",
            },
        ],
        "Good": [
            {
                "title": "Operating Systems: Three Easy Pieces (OSTEP)",
                "type": "Free Textbook",
                "url": "https://pages.cs.wisc.edu/~remzi/OSTEP/",
                "desc": "Renowned university textbook covering virtualization, concurrency, and persistence.",
            },
            {
                "title": "Linux Kernel Architecture & System Calls",
                "type": "Deep Dive",
                "url": "https://linuxjourney.com/",
                "desc": "Hands-on Linux system programming, bash scripting, and process memory maps.",
            },
        ],
    },
    "DBMS": {
        "Needs Improvement": [
            {
                "title": "SQL Tutorial - Full Database Course (freeCodeCamp)",
                "type": "Video Course",
                "url": "https://www.youtube.com/watch?v=HXV3zeRR3h4",
                "desc": "Learn SQL basics, schema design, SELECT queries, JOINs, and filtering.",
            },
            {
                "title": "W3Schools SQL Interactive Practice",
                "type": "Interactive Guide",
                "url": "https://www.w3schools.com/sql/",
                "desc": "Execute queries on sample databases directly in your browser.",
            },
        ],
        "Average": [
            {
                "title": "Normalization (1NF to BCNF) Made Simple",
                "type": "Conceptual Guide",
                "url": "https://www.geeksforgeeks.org/dbms/",
                "desc": "Step-by-step method for functional dependencies and lossless join decomposition.",
            },
            {
                "title": "LeetCode Database 50 SQL Study Plan",
                "type": "Problem Solving",
                "url": "https://leetcode.com/studyplan/top-sql-50/",
                "desc": "Curated 50 industry SQL challenges covering grouping, window functions, and subqueries.",
            },
        ],
        "Good": [
            {
                "title": "Database Internals & Indexing (B+ Trees & WAL)",
                "type": "System Design",
                "url": "https://use-the-index-luke.com/",
                "desc": "Deep dive into query execution engines, index optimizations, and ACID internals.",
            },
            {
                "title": "PostgreSQL High Performance Architecture",
                "type": "Advanced",
                "url": "https://www.postgresql.org/docs/current/performance-tips.html",
                "desc": "Learn query profiling with EXPLAIN ANALYZE and transaction isolation levels.",
            },
        ],
    },
    "Computer Networks": {
        "Needs Improvement": [
            {
                "title": "Computer Networking Complete Course - NetworkChuck",
                "type": "Video Playlist",
                "url": "https://www.youtube.com/playlist?list=PLIhvC56v63IJVXv0GJcl9vO5Z6znCVb1P",
                "desc": "Fun, visual introduction to IP addresses, Subnetting, Routers, Switches, and OSI Model.",
            },
            {
                "title": "OSI vs TCP/IP 7 Layers Simplified",
                "type": "Notes & Diagrams",
                "url": "https://www.geeksforgeeks.org/computer-network-tutorials/",
                "desc": "Layer-by-layer reference guide with standard port numbers and protocol duties.",
            },
        ],
        "Average": [
            {
                "title": "Subnetting Practice & IPv4 Classless Calculations",
                "type": "Interactive Practice",
                "url": "https://www.subnetting.org/",
                "desc": "Timed practice drills to solve CIDR and IP range calculation problems with ease.",
            },
            {
                "title": "TCP Handshake, Congestion Control & DNS Flow",
                "type": "Technical Guide",
                "url": "https://hpbn.co/",
                "desc": "High Performance Browser Networking by Ilya Grigorik - free online edition.",
            },
        ],
        "Good": [
            {
                "title": "Wireshark Packet Analysis Masterclass",
                "type": "Hands-on Lab",
                "url": "https://www.wireshark.org/docs/wsug_html_chunked/",
                "desc": "Inspect raw TCP packet captures, analyze TLS handshakes, and diagnose network drops.",
            },
            {
                "title": "Distributed Systems & Network Protocols Design",
                "type": "Advanced",
                "url": "https://github.com/donnemartin/system-design-primer",
                "desc": "Load balancers, CDN caching, reverse proxies, and RPC architecture.",
            },
        ],
    },
    "Machine Learning": {
        "Needs Improvement": [
            {
                "title": "StatQuest with Josh Starmer - ML Fundamentals",
                "type": "Video Playlist",
                "url": "https://www.youtube.com/playlist?list=PLblh5JKOoLUICTaGLRoHQDuF_7q2GfuJF",
                "desc": "Intuitive visual explanations of Linear Regression, Logistic Regression, and Decision Trees without confusing math jargon.",
            },
            {
                "title": "Scikit-Learn Getting Started Guide",
                "type": "Documentation",
                "url": "https://scikit-learn.org/stable/getting_started.html",
                "desc": "Clean walkthrough of train/test split, model fitting, and evaluation metrics.",
            },
        ],
        "Average": [
            {
                "title": "Feature Engineering & Model Evaluation (Kaggle)",
                "type": "Interactive Course",
                "url": "https://www.kaggle.com/learn/intro-to-machine-learning",
                "desc": "Hands-on Jupyter notebooks analyzing real-world datasets with Random Forests and XGBoost.",
            },
            {
                "title": "Hyperparameter Tuning & Cross-Validation Guide",
                "type": "Technical Guide",
                "url": "https://machinelearningmastery.com/",
                "desc": "Practical Python recipes for GridSearch, ROC-AUC, and handling imbalanced datasets.",
            },
        ],
        "Good": [
            {
                "title": "Deep Learning Specialization - Andrew Ng",
                "type": "Advanced Course",
                "url": "https://www.deeplearning.ai/",
                "desc": "Explore Neural Networks, Backpropagation, CNNs, and Transformer models.",
            },
            {
                "title": "MLOps & Model Deployment with FastAPI / Docker",
                "type": "Production Project",
                "url": "https://madewithml.com/",
                "desc": "End-to-end production ML pipeline from model tracking to automated deployment.",
            },
        ],
    },
    "HTML & CSS": {
        "Needs Improvement": [
            {
                "title": "HTML & CSS Full Course - Beginner to Pro (SuperSimpleDev)",
                "type": "Video Course",
                "url": "https://www.youtube.com/watch?v=G3e-cpL7ofc",
                "desc": "Complete hands-on beginner tutorial covering Flexbox, Grid, semantic HTML, and responsive UI.",
            },
            {
                "title": "MDN Web Docs - Learn HTML & CSS",
                "type": "Official Reference",
                "url": "https://developer.mozilla.org/en-US/docs/Learn",
                "desc": "Industry standard reference with clear interactive syntax snippets.",
            },
        ],
        "Average": [
            {
                "title": "Flexbox Froggy & CSS Grid Garden",
                "type": "Gamified Practice",
                "url": "https://flexboxfroggy.com/",
                "desc": "Interactive coding mini-games to cement CSS layout alignment and positioning.",
            },
            {
                "title": "Frontend Mentor UI Design Challenges",
                "type": "Projects",
                "url": "https://www.frontendmentor.io/",
                "desc": "Real-world web component templates to recreate from scratch with HTML & CSS.",
            },
        ],
        "Good": [
            {
                "title": "Modern CSS Animations, Transitions & Glassmorphism",
                "type": "Advanced Styling",
                "url": "https://css-tricks.com/almanac/",
                "desc": "Keyframe animations, custom CSS variables, and modern responsive container queries.",
            },
            {
                "title": "Web Accessibility (a11y) & Performance Optimization",
                "type": "Production Standards",
                "url": "https://web.dev/learn/",
                "desc": "Optimize Core Web Vitals, semantic landmarks, and screen reader compatibility.",
            },
        ],
    },
    "DSA": {
        "Needs Improvement": [
            {
                "title": "Data Structures & Algorithms in Python / Java (freeCodeCamp)",
                "type": "Video Course",
                "url": "https://www.youtube.com/watch?v=8hly31xKli0",
                "desc": "Comprehensive explanation of Arrays, Linked Lists, Stacks, Queues, and Big-O notation.",
            },
            {
                "title": "Visualgo.net - Algorithm Visualizer",
                "type": "Interactive Visualizer",
                "url": "https://visualgo.net/en",
                "desc": "Watch algorithms execute step-by-step with interactive visual animations.",
            },
        ],
        "Average": [
            {
                "title": "NeetCode 150 Curated DSA Roadmap",
                "type": "Coding Roadmap",
                "url": "https://neetcode.io/roadmap",
                "desc": "Categorized problem set from Binary Search, Trees to Two Pointers with video solutions.",
            },
            {
                "title": "GeeksforGeeks Top DSA Interview Questions",
                "type": "Question Bank",
                "url": "https://www.geeksforgeeks.org/must-do-coding-questions-for-companies-like-amazon-microsoft-adobe/",
                "desc": "Company-wise categorized list of frequently asked algorithmic problems.",
            },
        ],
        "Good": [
            {
                "title": "Dynamic Programming & Graph Theory Patterns",
                "type": "Advanced Problem Solving",
                "url": "https://leetcode.com/discuss/general-discussion/458695/dynamic-programming-patterns",
                "desc": "Comprehensive cheat sheet to master 0/1 Knapsack, LCS, Dijkstra, and Topological Sort.",
            },
            {
                "title": "Competitive Programming Handbook (Antti Laaksonen)",
                "type": "Free E-Book",
                "url": "https://cses.fi/book/book.pdf",
                "desc": "High-level algorithmic techniques used in coding olympiads and Google interviews.",
            },
        ],
    },
    "Python": {
        "Needs Improvement": [
            {
                "title": "Python for Beginners - Programming with Mosh",
                "type": "Video Course",
                "url": "https://www.youtube.com/watch?v=_uQrJ0TkZlc",
                "desc": "A fast, beginner-friendly introduction covering variables, loops, lists, and functions.",
            },
            {
                "title": "Python Cheatsheet & Interactive Shell",
                "type": "Interactive Guide",
                "url": "https://www.learnpython.org/",
                "desc": "Quick in-browser interactive lessons for clean Pythonic syntax.",
            },
        ],
        "Average": [
            {
                "title": "Real Python Tutorials & OOP in Python",
                "type": "Articles & Guides",
                "url": "https://realpython.com/",
                "desc": "In-depth tutorials on List Comprehensions, Decorators, Generators, and File I/O.",
            },
            {
                "title": "Exercism Python Track",
                "type": "Code Mentorship",
                "url": "https://exercism.org/tracks/python",
                "desc": "Solve 130+ structured exercises with automated test suites and community code reviews.",
            },
        ],
        "Good": [
            {
                "title": "Fluent Python - Modern Python Best Practices",
                "type": "Book Reference",
                "url": "https://github.com/fluentpython/example-code-2e",
                "desc": "Deep dive into dunder methods, concurrency with asyncio, and memory optimization.",
            },
            {
                "title": "Full-Stack Web Development with FastAPI",
                "type": "Project",
                "url": "https://fastapi.tiangolo.com/tutorial/",
                "desc": "Build lightning-fast async REST APIs with automatic Swagger documentation.",
            },
        ],
    },
    "Engineering Maths": {
        "Needs Improvement": [
            {
                "title": "3Blue1Brown - Essence of Linear Algebra & Calculus",
                "type": "Visual Math",
                "url": "https://www.youtube.com/c/3blue1brown",
                "desc": "Stunning geometric visualizations of vectors, matrices, eigenvalues, and derivatives.",
            },
            {
                "title": "Khan Academy - Multivariable Calculus & Linear Algebra",
                "type": "Interactive Math",
                "url": "https://www.khanacademy.org/math",
                "desc": "Step-by-step practice problems with video hints and concept recaps.",
            },
        ],
        "Average": [
            {
                "title": "Engineering Mathematics Gate Smashers Playlist",
                "type": "Exam Preparation",
                "url": "https://www.youtube.com/playlist?list=PLxCzCOWd7aiFe58n2qmyqA_rkygH2eHek",
                "desc": "Focus on high-yield exam topics: Probability distributions, Differential Equations, and Rank of Matrices.",
            },
            {
                "title": "Symbolab & Wolfram Alpha Step-by-Step Solvers",
                "type": "Problem Solver",
                "url": "https://www.symbolab.com/",
                "desc": "Verify answers and learn step-by-step solutions for integration, eigenvalues, and limits.",
            },
        ],
        "Good": [
            {
                "title": "MIT OpenCourseWare - Linear Algebra (Gilbert Strang)",
                "type": "University Lectures",
                "url": "https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/",
                "desc": "The gold-standard university series for true mathematical maturity.",
            },
            {
                "title": "Applied Numerical Methods & Optimization",
                "type": "Advanced Guide",
                "url": "https://numpy.org/doc/stable/user/absolute_beginners.html",
                "desc": "Implement mathematical algorithms in Python using NumPy and SciPy.",
            },
        ],
    },
    "Cloud Computing": {
        "Needs Improvement": [
            {
                "title": "Cloud Computing Fundamentals (freeCodeCamp)",
                "type": "Video Course",
                "url": "https://www.youtube.com/watch?v=2LaAJq1lB1Q",
                "desc": "Clear breakdown of IaaS, PaaS, SaaS, virtualization, and public vs private cloud models.",
            },
            {
                "title": "AWS Cloud Practitioner Essentials",
                "type": "Official Free Course",
                "url": "https://aws.amazon.com/training/digital/aws-cloud-practitioner-essentials/",
                "desc": "Free AWS digital course covering EC2, S3, IAM, and cloud security architecture.",
            },
        ],
        "Average": [
            {
                "title": "Docker & Containers Crash Course",
                "type": "Hands-on Lab",
                "url": "https://docker-curriculum.com/",
                "desc": "Practical guide to writing Dockerfiles, running containers, and pushing to Docker Hub.",
            },
            {
                "title": "Cloud Architecture & Serverless Computing",
                "type": "Reference",
                "url": "https://learn.microsoft.com/en-us/azure/architecture/",
                "desc": "Microsoft Azure architecture patterns for high-availability systems.",
            },
        ],
        "Good": [
            {
                "title": "Kubernetes The Hard Way (Kelsey Hightower)",
                "type": "Advanced Hands-on",
                "url": "https://github.com/kelseyhightower/kubernetes-the-hard-way",
                "desc": "Bootstrap a Kubernetes cluster from scratch to understand control planes and pods.",
            },
            {
                "title": "Terraform Infrastructure as Code (IaC)",
                "type": "DevOps Guide",
                "url": "https://developer.hashicorp.com/terraform/tutorials",
                "desc": "Provision and manage cloud infrastructure reliably using code.",
            },
        ],
    },
    "Data Science": {
        "Needs Improvement": [
            {
                "title": "Data Analysis with Python (freeCodeCamp)",
                "type": "Video Course",
                "url": "https://www.youtube.com/watch?v=r-uOLxNrNk8",
                "desc": "Learn Pandas, NumPy, Matplotlib, and data cleaning for real-world tabular data.",
            },
            {
                "title": "Kaggle Python & Pandas Micro-Courses",
                "type": "Interactive Notebooks",
                "url": "https://www.kaggle.com/learn/pandas",
                "desc": "Short, hands-on lessons to manipulate, filter, and aggregate datasets.",
            },
        ],
        "Average": [
            {
                "title": "Exploratory Data Analysis (EDA) Masterclass",
                "type": "Tutorial",
                "url": "https://towardsdatascience.com/",
                "desc": "Find correlations, treat outliers, and produce publishable visualizations with Seaborn.",
            },
            {
                "title": "Kaggle Community Competitions",
                "type": "Practice",
                "url": "https://www.kaggle.com/competitions",
                "desc": "Compete with data scientists globally and study top-ranking solution notebooks.",
            },
        ],
        "Good": [
            {
                "title": "End-to-End Data Science Portfolio Project",
                "type": "Portfolio Project",
                "url": "https://github.com/datastacktv/data-engineer-roadmap",
                "desc": "Build automated ETL pipelines, dashboard visualizations, and predictive models.",
            },
            {
                "title": "Big Data with Apache Spark & PySpark",
                "type": "Big Data Tool",
                "url": "https://spark.apache.org/docs/latest/api/python/",
                "desc": "Process terabyte-scale distributed datasets with PySpark DataFrames.",
            },
        ],
    },
    "Software Engineering": {
        "Needs Improvement": [
            {
                "title": "Software Engineering Methodologies - SDLC & Agile",
                "type": "Video Lecture",
                "url": "https://www.youtube.com/watch?v=sB2iQSvrrG0",
                "desc": "Understand Waterfall vs Agile Scrum, Sprint planning, and requirements engineering.",
            },
            {
                "title": "Git & GitHub Crash Course for Beginners",
                "type": "Interactive Tutorial",
                "url": "https://learngitbranching.js.org/",
                "desc": "Visual interactive playground to master git commits, branches, merges, and rebasing.",
            },
        ],
        "Average": [
            {
                "title": "Clean Code Principles & SOLID Design",
                "type": "Reading Guide",
                "url": "https://www.freecodecamp.org/news/solid-principles-explained-in-plain-english/",
                "desc": "Learn Single Responsibility, Open-Closed, and Dependency Inversion with clear examples.",
            },
            {
                "title": "Unit Testing & Test Driven Development (TDD)",
                "type": "Testing Guide",
                "url": "https://martinfowler.com/articles/practical-test-pyramid.html",
                "desc": "How to structure unit, integration, and end-to-end tests effectively.",
            },
        ],
        "Good": [
            {
                "title": "Microservices vs Monolith Architecture Guide",
                "type": "Architecture Guide",
                "url": "https://microservices.io/patterns/index.html",
                "desc": "Deconstruct complex business domains into scalable microservices.",
            },
            {
                "title": "CI/CD Automation with GitHub Actions",
                "type": "DevOps Guide",
                "url": "https://docs.github.com/en/actions",
                "desc": "Build automated test runners and deployment pipelines triggered on every pull request.",
            },
        ],
    },
    "Web Technologies": {
        "Needs Improvement": [
            {
                "title": "Web Development Full Stack Roadmap 2026",
                "type": "Video Guide",
                "url": "https://www.youtube.com/watch?v=nu_pCVPKzTk",
                "desc": "Clear breakdown of Frontend (HTML/CSS/JS) and Backend client-server request cycles.",
            },
            {
                "title": "JavaScript.info - The Modern JavaScript Tutorial",
                "type": "Interactive Tutorial",
                "url": "https://javascript.info/",
                "desc": "From fundamentals to advanced topics with simple explanations and tasks.",
            },
        ],
        "Average": [
            {
                "title": "Fetch API, Async/Await & RESTful Endpoints",
                "type": "Tutorial",
                "url": "https://developer.mozilla.org/en-US/docs/Learn/JavaScript/Client-side_web_APIs/Fetching_data",
                "desc": "Connect your frontend UI dynamically to backend REST APIs using JSON.",
            },
            {
                "title": "Frontend Frameworks: React or Vue Beginner Docs",
                "type": "Framework Guide",
                "url": "https://react.dev/learn",
                "desc": "Build reactive component-based user interfaces with modern React hooks.",
            },
        ],
        "Good": [
            {
                "title": "Full-Stack Web Security (OWASP Top 10)",
                "type": "Security Guide",
                "url": "https://owasp.org/www-project-top-ten/",
                "desc": "Protect web apps against SQL injection, XSS attacks, and CSRF vulnerabilities.",
            },
            {
                "title": "WebSockets, Real-time Communication & PWAs",
                "type": "Advanced Architecture",
                "url": "https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API",
                "desc": "Implement real-time bidirectional communication for live chats and dashboards.",
            },
        ],
    },
    "Advanced Java": {
        "Needs Improvement": [
            {
                "title": "Java JDBC & Database Connectivity Tutorial",
                "type": "Video Course",
                "url": "https://www.youtube.com/watch?v=2i4t-SL1kVU",
                "desc": "Connect Java applications to MySQL/PostgreSQL databases using PreparedStatement.",
            },
            {
                "title": "Java Servlets & JSP Fundamentals",
                "type": "Notes & Tutorials",
                "url": "https://www.javatpoint.com/servlet-tutorial",
                "desc": "Understand HTTP GET/POST lifecycles, Sessions, and Cookies in Java web apps.",
            },
        ],
        "Average": [
            {
                "title": "Hibernate ORM & JPA Entity Mapping",
                "type": "Documentation",
                "url": "https://hibernate.org/orm/documentation/",
                "desc": "Map relational database tables directly to Java classes using Hibernate annotations.",
            },
            {
                "title": "Java Multithreading & Concurrency Utilities",
                "type": "Guide",
                "url": "https://www.baeldung.com/java-concurrency",
                "desc": "ExecutorService, CountDownLatch, and thread-safe collections in java.util.concurrent.",
            },
        ],
        "Good": [
            {
                "title": "Spring Boot Security (JWT & OAuth2)",
                "type": "Enterprise Tutorial",
                "url": "https://www.baeldung.com/spring-security-login",
                "desc": "Implement enterprise-grade token-based authentication and role-based access control.",
            },
            {
                "title": "Reactive Programming in Java with Project Reactor",
                "type": "Advanced",
                "url": "https://projectreactor.io/docs/core/release/reference/",
                "desc": "Non-blocking reactive microservices using Mono, Flux, and Spring WebFlux.",
            },
        ],
    },
    "Algorithms": {
        "Needs Improvement": [
            {
                "title": "Sorting & Searching Algorithms Visualized",
                "type": "Visual Guide",
                "url": "https://visualgo.net/en/sorting",
                "desc": "Interactive step-by-step animations of Bubble, Merge, Quick Sort and Binary Search.",
            },
            {
                "title": "Algorithm Analysis & Asymptotic Big-O Tutorial",
                "type": "Reading Guide",
                "url": "https://www.geeksforgeeks.org/analysis-of-algorithms-set-1-asymptotic-analysis/",
                "desc": "Master how to evaluate time and space complexity of loops and recursive calls.",
            },
        ],
        "Average": [
            {
                "title": "Greedy Algorithms & Divide and Conquer Patterns",
                "type": "Problem Solving",
                "url": "https://www.geeksforgeeks.org/fundamentals-of-algorithms/",
                "desc": "Huffman Coding, Fractional Knapsack, Activity Selection, and Strassen's matrix multiplication.",
            },
            {
                "title": "LeetCode Medium Algorithm Study Pack",
                "type": "Coding Challenges",
                "url": "https://leetcode.com/problemset/all/?difficulty=MEDIUM",
                "desc": "Solve standard intermediate algorithm interview questions.",
            },
        ],
        "Good": [
            {
                "title": "Advanced Graph Theory (Network Flow & Max-Cut)",
                "type": "Advanced Algorithmics",
                "url": "https://cp-algorithms.com/",
                "desc": "Ford-Fulkerson, Dinic's Algorithm, Bellman-Ford, and Tarjan's strongly connected components.",
            },
            {
                "title": "NP-Completeness & Approximation Algorithms",
                "type": "Theoretical CS",
                "url": "https://ocw.mit.edu/courses/6-046j-design-and-analysis-of-algorithms-spring-2015/",
                "desc": "MIT graduate series covering polynomial reductions, SAT solvers, and randomized algorithms.",
            },
        ],
    },
}

DEFAULT_RESOURCES = {
    "Needs Improvement": [
        {
            "title": "Core Fundamentals & Video Lecture Series",
            "type": "Video Playlist",
            "url": "https://www.youtube.com/results?search_query=computer+science+fundamentals",
            "desc": "Foundational tutorials covering basic concepts and core definitions step-by-step.",
        },
        {
            "title": "GeeksforGeeks Academic Revision Notes",
            "type": "Notes & Cheatsheet",
            "url": "https://www.geeksforgeeks.org/",
            "desc": "Quick revision notes with diagrams, examples, and exam-oriented definitions.",
        },
    ],
    "Average": [
        {
            "title": "Subject Question Bank & Solved Examples",
            "type": "Practice Problems",
            "url": "https://www.sanfoundry.com/",
            "desc": "Solve subject-wise numerical and conceptual questions to bridge the gap to top marks.",
        },
        {
            "title": "Interactive Problem Solving & Quizzes",
            "type": "Quiz & Exercises",
            "url": "https://www.tutorialspoint.com/",
            "desc": "Reinforce knowledge through bite-sized interactive quizzes and chapter tests.",
        },
    ],
    "Good": [
        {
            "title": "Advanced Mastery & System Architecture",
            "type": "Advanced Reference",
            "url": "https://github.com/developer-roadmap",
            "desc": "Explore real-world software architecture and production-grade applications.",
        },
        {
            "title": "Industry Best Practices & Open-Source Projects",
            "type": "Hands-on Projects",
            "url": "https://github.com/",
            "desc": "Build portfolio projects and study production implementations on GitHub.",
        },
    ],
}


def get_recommended_resources(info, marks):
    """
    Build prioritized list of recommended learning resources based on student performance.
    Groups subjects into:
      1. High Priority (Needs Improvement / Low Marks)
      2. Moderate Priority (Average)
      3. Mastery / Advanced (Good)
    """
    # Sort subjects: worst percentile first
    sorted_subjects = sorted(info.keys(), key=lambda s: info[s]["percentile"])

    categories = [
        {"key": "Needs Improvement", "badge": "High Priority", "badge_class": "badge-bad"},
        {"key": "Average", "badge": "Medium Priority", "badge_class": "badge-avg"},
        {"key": "Good", "badge": "Mastery", "badge_class": "badge-good"},
    ]

    recommendations = []

    for cat in categories:
        cat_key = cat["key"]
        cat_subjects = [s for s in sorted_subjects if info[s]["label"] == cat_key]

        if not cat_subjects:
            continue

        for subj in cat_subjects:
            # Lookup resource
            subj_dict = SUBJECT_RESOURCES.get(subj, DEFAULT_RESOURCES)
            res_list = subj_dict.get(cat_key, DEFAULT_RESOURCES.get(cat_key, []))

            recommendations.append({
                "subject": subj,
                "score": marks.get(subj, 0),
                "label": info[subj]["label"],
                "target": info[subj]["target"],
                "need": info[subj]["need"],
                "priority_badge": cat["badge"],
                "priority_class": cat["badge_class"],
                "resources": res_list,
            })

    return recommendations
