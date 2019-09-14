export const BLACK = '#000000';
export const WHITE = '#ffffff';
export const SQUARE_BRACKET = 'square-bracket';

export const COLOR_SCHEME = {
    0: '#5ffe56',
    1: '#9cf4e8', 
    2: '#d42673', 
    3: '#dfa934', 
    4: '#44d304', 
    5: '#87cac4',
    6: '#6995b2', 
    7: '#10d805', 
    8: '#6f7319', 
    9: '#1a0c45', 
    10: '#af0396',
    11: '#a4d265', 
    12: '#87cbd7', 
    13: '#1803e4', 
    14: '#830f59', 
    15: '#82a8e1',
    16: '#034fd6', 
    17: '#3fe667', 
    18: '#4f83f2', 
    19: '#bf7561', 
    20: '#c0f3f7',
    21: '#eff169', 
    22: '#da2826', 
    23: '#5a6096', 
    24: '#00ad73', 
    25: '#bb7521',
    26: '#dac112', 
    27: '#6a3ab6', 
    28: '#744d09', 
    29: '#e9e672', 
    30: '#c76348',
    31: '#cba1d5', 
    32: '#3ecf21', 
    33: '#02f2f6', 
    34: '#b61629', 
    35: '#ab1177',
};

export const ALL_SYMBOLS = {
    value: -1,
    label: 'Все символы'
}

function getOptions(input, href, additional) {
    return fetch(`${href}?q=${input}${additional ? '&' + additional : ''}`, {credentials: 'same-origin'})
        .then((response) => {
            return response.json()
        }).then((json) => {
            return json.result;
        });
}

export const getContexts = (input) => getOptions(input, '/editor/contexts/');
export const getContextTypes = (input) => getOptions(input, '/editor/context_types')

export function getCollors(NumCоlor) {
    // число шагов внутри каждого тона цветовой RGB-составляющей
    step = Math.round( Math.pow(NumCоlor , 1./3)-1);

    // размер шагов внутри каждого тона цветовой RGB-составляющей
    step_tone = Math.round(0xFF/step);

    // массив из которого будем дергать цвета 
    DimColor = [];
    for (i1=0; i1<=step; i1++ ) {
        for (i2=step; i2>=0; i2-- ) {
            for (i3=0; i3<=step; i3++ ) {
                // помещаем цвет в массив
                DimColor.push("rgb("+i1*step_tone+","+i2*step_tone+","+i3*step_tone+")");
            }
        }
    }
}

function RGBToHSL(r,g,b) {
    let { h, s, l} = getParams(r,g,b)
    return "hsl(" + h + "," + s + "%," + l + "%)";
}

function getParams(r,g,b) {
    r /= 255;
    g /= 255;
    b /= 255;

    let cmin = Math.min(r,g,b),
        cmax = Math.max(r,g,b),
        delta = cmax - cmin,
        h = 0,
        s = 0,
        l = 0;

    if (delta == 0)
        h = 0;
    else if (cmax == r)
        h = ((g - b) / delta) % 6;
    else if (cmax == g)
        h = (b - r) / delta + 2;
    else
        h = (r - g) / delta + 4;

    h = Math.round(h * 60);
    if (h < 0)
        h += 360;

    l = (cmax + cmin) / 2;
    l = +(l * 100).toFixed(1);
    s = delta == 0 ? 0 : delta / (1 - Math.abs(2 * l - 1));
    s = +(s * 100).toFixed(1);

    return { h, s, l};
}

function renderPalitra() {
    let rgbs = [];
    let variants = [0, 16, 32, 48, 64, 80, 96, 112, 128, 144, 160, 176, 192, 208, 224, 240, 256];
    for (let i of variants) {
        for (let j of variants) {
            for (let k of variants) {
                rgbs.push([i, j, k]);
            }
        }
    }

    let hsls = [];
    for (let rgb of rgbs) {
        let {h, s, l} = getParams(rgb[0], rgb[1], rgb[2]);
        hsls.push([h, s, l]);
    }

    function myCompare(a,b) {
        if (a[0] != b[0]) {
            return a[0] - b[0];
        } else if (a[1] != b[1]) {
            return a[1] - b[1];
        } else if (a[2] != b[2]) {
            return a[2] - b[2];
        } else {
            return 0;
        }
    }

    hsls.sort(myCompare);

    for (let hsl of hsls){
        let col = "hsl(" + hsl[0] + "," + hsl[1] + "%," + hsl[2] + "%)";
        document.write("<span style='color:"+col + ";'>█</span>");
    }
}