### PHP XSS Vulnerabilities
- [ссылка 1](https://www.cvedetails.com/vulnerability-search.php?f=1&vendor=&product=%25php%25&cveid=CVE-2021%25&msid=&bidno=&cweid=&cvssscoremin=&cvssscoremax=&psy=2021&psm=1&pey=2022&pem=1&usy=&usm=&uey=&uem=&opxss=1)
- [ссылка 2](https://www.cvedetails.com/vulnerability-list/vendor_id-74/year-2021/PHP.html)


<i>Из таблицы ниже убраны CVE-2020</i>

|#|Description|Code|CWE ID|
|-|-|-|-|
|1|PHP Event Calendar through 2021-11-04 allows persistent cross-site scripting (XSS), as demonstrated by the /server/ajax/events_manager.php title parameter. This can be exploited by an adversary in multiple ways, e.g., to perform actions on the page in the context of other users, or to deface the site|[CVE-2021-42078](https://nvd.nist.gov/vuln/detail/CVE-2021-42078)|[79](https://www.security-database.com/cwe.php?name=CWE-79)|
|2|PHPFusion 9.03.110 is affected by cross-site scripting (XSS) in the preg patterns filter html tag without "//" in descript() function An authenticated user can trigger XSS by appending "//" in the end of text|[CVE-2021-40541](https://nvd.nist.gov/vuln/detail/CVE-2021-40541)|[79](https://www.security-database.com/cwe.php?name=CWE-79)|
|3|CSRF + Cross-site scripting (XSS) vulnerability in search.php in PHPFusion 9.03.110 allows remote attackers to inject arbitrary web script or HTML|[CVE-2021-28280](https://nvd.nist.gov/vuln/detail/CVE-2021-28280)|[352](https://www.security-database.com/cwe.php?name=CWE-352)|
|4|Cross Site Scripting (XSS) in the "add-services.php" component of PHPGurukul Beauty Parlour Management System v1.0 allows remote attackers to execute arbitrary code by injecting arbitrary HTML into the "sername" parameter|[CVE-2021-27544](https://nvd.nist.gov/vuln/detail/CVE-2021-27544)|[79](https://www.security-database.com/cwe.php?name=CWE-79)|
|5|phpIPAM 1.4.3 allows Reflected XSS via app/dashboard/widgets/ipcalc-result.php and app/tools/ip-calculator/result.php of the IP calculator|[CVE-2021-35438](https://nvd.nist.gov/vuln/detail/CVE-2021-35438)|[79](https://www.security-database.com/cwe.php?name=CWE-79)|
|6|phpWhois (last update Jun 30 2021) is affected by a Cross Site Scripting (XSS) vulnerability. In file example.php, the exit function will terminate the script and print the message to the user. The message will contain $_GET['query'] then there is a XSS vulnerability|[CVE-2021-43698](https://nvd.nist.gov/vuln/detail/CVE-2021-43698)|[79](https://www.security-database.com/cwe.php?name=CWE-79)|
|7*|phpLiteAdmin through 1.9.8.2 allows XSS via the index.php newRows parameter (aka num or number)|[CVE-2021-46709](https://nvd.nist.gov/vuln/detail/CVE-2021-46709)|[79](https://www.security-database.com/cwe.php?name=CWE-79)|
<br/>

---

### CVSS Scores For PHP Products 2021

- [ссылка](https://www.cvedetails.com/cvss-score-charts.php?fromform=1&vendor_id=74&product_id=&startdate=2021-01-01&enddate=2021-12-31) (с учетом уязвимостей CVE-2020)

|CVSS Score|Number Of Vulnerabilities|Percentage|
|-|-|-|
|0-1|0|0|
|1-2|0|0|
|2-3|0|0|
|3-4|1|12.50|
|4-5|1|12.50|
|5-6|5|62.50|
|6-7|1|12.50|
|7-8|0|0|
|8-9|0|0|
|9-10|0|0|
|<b>Total</b>|<b>8</b>|

<br/>

---

### CVSS Scores 2021

- [ссылка](https://www.cvedetails.com/cvss-score-charts.php?fromform=1&vendor_id=&product_id=&startdate=2021-01-01&enddate=2021-12-31)

|CVSS Score|Number Of Vulnerabilities|Percentage|
|-|-|-|
|0-1|170|0.80|
|1-2|90|0.40|
|2-3|1225|6.10|
|3-4|1827|9.10|
|4-5|5470|27.10|
|5-6|3672|18.20|
|6-7|3690|18.30|
|7-8|2723|13.50|
|8-9|131|0.60|
|9-10|1170|5.80|
|<b>Total</b>|<b>20168</b>|| 	