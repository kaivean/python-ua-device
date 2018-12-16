

var parseUA = require('../js/ua-device');
var fs = require('fs');

// let data = fs.readFileSync('data.txt', 'utf8');
let data = fs.readFileSync('data10000.txt', 'utf8');

let uas = data.split('\n');

let diffs = [
    37,
    39,
    81,
    107,
    195,
    213,
    234,
    239,
    258,
    298,
    344,
    345,
    428,
    429,
    481,
    529,
    530,
    536,
    544,
    559,
    574,
    581,
    587,
    621,
    622,
    632,
    640,
    643,
    664,
    692,
    702,
    704,
    705
];
// js => python
// ZTEQ801U//345 mobile	Q801	Zte  -> tablet	Q801U  Zte
// mobile	S76	Vivo  -> tablet	S76	Vivo
// MI-4    MI-4LTE
//37 MI-6   MI-6X
// HM-UNDEFINED  HM-NONE
//195 MI-5 ->  MI-5X
//587 Chrome	39.0.2171.95  -> 	Microsoft Edge	12
// GT-I920	Samsung -> GT-I9208	Samsung
//559 mobile	JDN-AL00	Huawei -> tablet	JDN-AL00	Huawei
//544 A602	Zte -> BA602T	Zte
//344 mobile	READBOY-G90S -> tablet	READBOY-G90S
//234 UC Browser	11.9.6.976 -> Microsoft Edge	12
//107 CHE	Huawei -> CHE2	Huawei
let s = Date.now();
uas.forEach((ua, i) => {
    // if (i + 1 != 7402) {
    //     return;
    // }
    // console.log('ua', i, ua, ua.length);
    // let match = ua.match(/[-\s](Galaxy[\s-_]nexus|Galaxy[\s-_]\w*[\s-_]\w*|Galaxy[\s-_]\w*|SM-\w*|GT-\w*|s[cgp]h-\w*|shw-\w*|ATIV|i9070|omnia|s7568|A3000|A3009|A5000|A5009|A7000|A7009|A8000|C101|C1116|C1158|E400|E500F|E7000|E7009|G3139D|G3502|G3502i|G3508|G3508J|G3508i|G3509|G3509i|G3558|G3559|G3568V|G3586V|G3589W|G3606|G3608|G3609|G3812|G388F|G5108|G5108Q|G5109|G5306W|G5308W|G5309W|G550|G600|G7106|G7108|G7108V|G7109|G7200|G720NO|G7508Q|G7509|G8508S|G8509V|G9006V|G9006W|G9008V|G9008W|G9009D|G9009W|G9198|G9200|G9208|G9209|G9250|G9280|I535|I679|I739|I8190N|I8262|I879|I879E|I889|I9000|I9060|I9082|I9082C|I9082i|I9100|I9100G|I9108|I9128|I9128E|I9128i|I9152|I9152P|I9158|I9158P|I9158V|I9168|I9168i|I9190|I9192|I9195|I9195I|I9200|I9208|I9220|I9228|I9260|I9268|I9300|I9300i|I9305|I9308|I9308i|I939|I939D|I939i|I9500|I9502|I9505|I9507V|I9508|I9508V|I959|J100|J110|J5008|J7008|N7100|N7102|N7105|N7108|N7108D|N719|N750|N7505|N7506V|N7508V|N7509V|N900|N9002|N9005|N9006|N9008|N9008S|N9008V|N9009|N9100|N9106W|N9108V|N9109W|N9150|N916|N9200|P709|P709E|P729|S6358|S7278|S7278U|S7562C|S7562i|S7898i|b9388)[\s\)]/i);
    // console.log('match', match);
    let info = parseUA(ua);

    console.log(
        [
            info['os']['name'],
            info['os']['version'] && info['os']['version']['original'],
            info['browser']['name'],
            info['browser']['version'] && info['browser']['version']['original'],
            info['engine']['name'],
            info['engine']['version'] && info['engine']['version']['original'],
            info['device']['type'],
            info['device']['model'],
            info['device']['manufacturer']
        ].join('\t')
    );

});
console.error('time', Date.now() - s);