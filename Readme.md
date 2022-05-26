<div id="top"></div>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->


<!-- PROJECT LOGO -->
<br />
<div align="center">
  <h3 align="center">Mocking FW Logs</h3>

  <p align="center">
    Generate mock FW logs to testing your Application, SQL or SPL
    <br />
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

![Project][product-screenshot]

There was some needs to testing my SPL in live time. But, there were no resources because, I could not took out logs of FW / IPS in my company, and test my SPL in environment of my company because of the security limitation.</br>
So, I write this script which mock the firewall logs simply.</br>
You can utilize this naive script just changing the configuration or can modify some codes for your own needs.</br>

* I also offer some scripts generating logs which have relation with attackers behavior. So, you can utilze this scripts to testing your Network Monitoring System at the point of Cyber Security Manager.
  

<p align="right">(<a href="#top">back to top</a>)</p>

### Built With

You just need Python3 to launch this script.
* [Python3](https://www.python.org)



<!-- GETTING STARTED -->
<br>

## Getting Started
### Prerequisites

This code is so simple, so you should just install the numpy Python3 module with pip3
  ```sh
  pip3 install numpy
  ```

### Installation
```sh
   git clone https://github.com/orca-eaa5a/mock-fw-log.git
```

<!-- USAGE EXAMPLES -->
## Usage
![Configureation][configure-screenshot]
Before launch the main script ***generate.py***, we have to configure the mock network setting which impact the logs.</br>The configuration is JSON like format.
You can also set the ***weight***. If ***weight*** is bigger, the frequency of the log impacted with ***weight*** setting increase.</br>
In current version(0.0.1) only support 3 protocols. And there is no FW rule configuration, ***so denied/allowed log is generated randomly.***
</br>

![Configureation][malconfigure-screenshot]
You can also set malicious log generator settings if you need.


<!-- ROADMAP -->
## Roadmap

- [x] Mock Firwall Logs and implement generator
- [x] Mock Suspicious log and implement generator
- [ ] Implement user configured firewall rule based log generating method



<!-- LICENSE -->
## License

Distributed under the MIT License.


<!-- CONTACT -->
## Contact

@mail : orca_eaa5a@naver.com / @github : [https://github.com/orca-eaa5a](https://github.com/orca-eaa5a)


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->

[product-screenshot]: resource/result.png
[configure-screenshot]: resource/configure.png
[malconfigure-screenshot]: resource/mal-configure.png