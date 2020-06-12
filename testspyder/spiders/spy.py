
import os
import re
import json

import scrapy, time, hmac, base64
from urllib.parse import urlencode
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from hashlib import sha1
from scrapy import Selector
import execjs
from urllib import parse


'''js code'''
tecode = r'''
window = {
    navigator: {
        userAgent: "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36"
    }
}
function f(module, exports, __webpack_require__) {
    "use strict";
    function t(e) {
        return (t = "function" == typeof Symbol && "symbol" == typeof Symbol.A ? function(e) {
            return typeof e
        }
        : function(e) {
            return e && "function" == typeof Symbol && e.constructor === Symbol && e !== Symbol.prototype ? "symbol" : typeof e
        }
        )(e)
    }
    exports['__esModule'] = !0
    var A = "2.0"
      , __g = {};
    function s() {}
    function i(e) {
        this.t = (2048 & e) >> 11,
        this.s = (1536 & e) >> 9,
        this.i = 511 & e,
        this.h = 511 & e
    }
    function h(e) {
        this.s = (3072 & e) >> 10,
        this.h = 1023 & e
    }
    function a(e) {
        this.a = (3072 & e) >> 10,
        this.c = (768 & e) >> 8,
        this.n = (192 & e) >> 6,
        this.t = 63 & e
    }
    function c(e) {
        this.s = e >> 10 & 3,
        this.i = 1023 & e
    }
    function n() {}
    function e(e) {
        this.a = (3072 & e) >> 10,
        this.c = (768 & e) >> 8,
        this.n = (192 & e) >> 6,
        this.t = 63 & e
    }
    function o(e) {
        this.h = (4095 & e) >> 2,
        this.t = 3 & e
    }
    function r(e) {
        this.s = e >> 10 & 3,
        this.i = e >> 2 & 255,
        this.t = 3 & e
    }
    s.prototype.e = function(e) {
        e.o = !1
    }  
    i.prototype.e = function(e) {
        switch (this.t) {
        case 0:
            e.r[this.s] = this.i;
            break;
        case 1:
            e.r[this.s] = e.k[this.h]
        }
    }
    h.prototype.e = function(e) {
        e.k[this.h] = e.r[this.s]
    }    
    a.prototype.e = function(e) {
        switch (this.t) {
        case 0:
            e.r[this.a] = e.r[this.c] + e.r[this.n];
            break;
        case 1:
            e.r[this.a] = e.r[this.c] - e.r[this.n];
            break;
        case 2:
            e.r[this.a] = e.r[this.c] * e.r[this.n];
            break;
        case 3:
            e.r[this.a] = e.r[this.c] / e.r[this.n];
            break;
        case 4:
            e.r[this.a] = e.r[this.c] % e.r[this.n];
            break;
        case 5:
            e.r[this.a] = e.r[this.c] == e.r[this.n];
            break;
        case 6:
            e.r[this.a] = e.r[this.c] >= e.r[this.n];
            break;
        case 7:
            e.r[this.a] = e.r[this.c] || e.r[this.n];
            break;
        case 8:
            e.r[this.a] = e.r[this.c] && e.r[this.n];
            break;
        case 9:
            e.r[this.a] = e.r[this.c] !== e.r[this.n];
            break;
        case 10:
            e.r[this.a] = t(e.r[this.c]);
            break;
        case 11:
            e.r[this.a] = e.r[this.c]in e.r[this.n];
            break;
        case 12:
            e.r[this.a] = e.r[this.c] > e.r[this.n];
            break;
        case 13:
            e.r[this.a] = -e.r[this.c];
            break;
        case 14:
            e.r[this.a] = e.r[this.c] < e.r[this.n];
            break;
        case 15:
            e.r[this.a] = e.r[this.c] & e.r[this.n];
            break;
        case 16:
            e.r[this.a] = e.r[this.c] ^ e.r[this.n];
            break;
        case 17:
            e.r[this.a] = e.r[this.c] << e.r[this.n];
            break;
        case 18:
            e.r[this.a] = e.r[this.c] >>> e.r[this.n];
            break;
        case 19:
            e.r[this.a] = e.r[this.c] | e.r[this.n];
            break;
        case 20:
            e.r[this.a] = !e.r[this.c]
        }
    }
    c.prototype.e = function(e) {
        e.Q.push(e.C),
        e.B.push(e.k),
        e.C = e.r[this.s],
        e.k = [];
        for (var t = 0; t < this.i; t++)
            e.k.unshift(e.f.pop());
        e.g.push(e.f),
        e.f = []
    }
    
    n.prototype.e = function(e) {
        e.C = e.Q.pop(),
        e.k = e.B.pop(),
        e.f = e.g.pop()
    }
    
    e.prototype.e = function(e) {
        switch (this.t) {
        case 0:
            e.u = e.r[this.a] >= e.r[this.c];
            break;
        case 1:
            e.u = e.r[this.a] <= e.r[this.c];
            break;
        case 2:
            e.u = e.r[this.a] > e.r[this.c];
            break;
        case 3:
            e.u = e.r[this.a] < e.r[this.c];
            break;
        case 4:
            e.u = e.r[this.a] == e.r[this.c];
            break;
        case 5:
            e.u = e.r[this.a] != e.r[this.c];
            break;
        case 6:
            e.u = e.r[this.a];
            break;
        case 7:
            e.u = !e.r[this.a]
        }
    }
    
    o.prototype.e = function(e) {
        switch (this.t) {
        case 0:
            e.C = this.h;
            break;
        case 1:
            e.u && (e.C = this.h);
            break;
        case 2:
            e.u || (e.C = this.h);
            break;
        case 3:
            e.C = this.h,
            e.w = null
        }
        e.u = !1
    }
    r.prototype.e = function(e) {
        switch (this.t) {
        case 0:
            for (var t = [], n = 0; n < this.i; n++)
                t.unshift(e.f.pop());
            e.r[3] = e.r[this.s](t[0], t[1]);
            break;
        case 1:
            for (var r = e.f.pop(), i = [], o = 0; o < this.i; o++)
                i.unshift(e.f.pop());
            e.r[3] = e.r[this.s][r](i[0], i[1]);
            break;
        case 2:
            for (var a = [], s = 0; s < this.i; s++)
                a.unshift(e.f.pop());
            e.r[3] = new e.r[this.s](a[0],a[1])
        }
    }
    var k = function(e) {
        for (var t = 66, n = [], r = 0; r < e.length; r++) {
            var i = 24 ^ e.charCodeAt(r) ^ t;
            n.push(String.fromCharCode(i)),
            t = i
        }
        return n.join("")
    }
    function Q(e) {
        this.t = (4095 & e) >> 10,
        this.s = (1023 & e) >> 8,
        this.i = 1023 & e,
        this.h = 63 & e
    }
    function C(e) {
        this.t = (4095 & e) >> 10,
        this.a = (1023 & e) >> 8,
        this.c = (255 & e) >> 6
    }
    function B(e) {
        this.s = (3072 & e) >> 10,
        this.h = 1023 & e
    }
    function f(e) {
        this.h = 4095 & e
    }
    function g(e) {
        this.s = (3072 & e) >> 10
    }
    function u(e) {
        this.h = 4095 & e
    }
    function w(e) {
        this.t = (3840 & e) >> 8,
        this.s = (192 & e) >> 6,
        this.i = 63 & e
    }
    function G() {
        this.r = [0, 0, 0, 0],
        this.C = 0,
        this.Q = [],
        this.k = [],
        this.B = [],
        this.f = [],
        this.g = [],
        this.u = !1,
        this.G = [],
        this.b = [],
        this.o = !1,
        this.w = null,
        this.U = null,
        this.F = [],
        this.R = 0,
        this.J = {
            0: s,
            1: i,
            2: h,
            3: a,
            4: c,
            5: n,
            6: e,
            7: o,
            8: r,
            9: Q,
            10: C,
            11: B,
            12: f,
            13: g,
            14: u,
            15: w
        }
    }            
    Q.prototype.e = function(e) {
        switch (this.t) {
        case 0:
            e.f.push(e.r[this.s]);
            break;
        case 1:
            e.f.push(this.i);
            break;
        case 2:
            e.f.push(e.k[this.h]);
            break;
        case 3:
            e.f.push(k(e.b[this.h]))
        }
    }
    
    C.prototype.e = function(A) {
        switch (this.t) {
        case 0:
            var t = A.f.pop();
            A.r[this.a] = A.r[this.c][t];
            break;
        case 1:
            var s = A.f.pop()
              , i = A.f.pop();
            A.r[this.c][s] = i;
            break;
        case 2:
            var h = A.f.pop();
            A.r[this.a] = eval(h)
        }
    }
    
    B.prototype.e = function(e) {
        e.r[this.s] = k(e.b[this.h])
    }
    
    f.prototype.e = function(e) {
        e.w = this.h
    }
    
    g.prototype.e = function(e) {
        throw e.r[this.s]
    }
    
    u.prototype.e = function(e) {
        var t = this
          , n = [0];
        e.k.forEach(function(e) {
            n.push(e)
        });
        var r = function(r) {
            var i = new G;
            return i.k = n,
            i.k[0] = r,
            i.v(e.G, t.h, e.b, e.F),
            i.r[3]
        };
        r.toString = function() {
            return "() { [native code] }"
        }
        ,
        e.r[3] = r
    }
    
    w.prototype.e = function(e) {
        switch (this.t) {
        case 0:
            for (var t = {}, n = 0; n < this.i; n++) {
                var r = e.f.pop();
                t[e.f.pop()] = r
            }
            e.r[this.s] = t;
            break;
        case 1:
            for (var i = [], o = 0; o < this.i; o++)
                i.unshift(e.f.pop());
            e.r[this.s] = i
        }
    }
    
    G.prototype.D = function(e) {
        for (var t = atob(e), n = t.charCodeAt(0) << 8 | t.charCodeAt(1), r = [], i = 2; i < n + 2; i += 2)
            r.push(t.charCodeAt(i) << 8 | t.charCodeAt(i + 1));
        this.G = r;
        for (var o = [], a = n + 2; a < t.length; ) {
            var s = t.charCodeAt(a) << 8 | t.charCodeAt(a + 1)
              , c = t.slice(a + 2, a + 2 + s);
            o.push(c),
            a += s + 2
        }
        this.b = o
    }
    
    G.prototype.v = function(e, t, n) {
        for (t = t || 0,
        n = n || [],
        this.C = t,
        "string" == typeof e ? this.D(e) : (this.G = e,
        this.b = n),
        this.o = !0,
        this.R = Date.now(); this.o; ) {
            var r = this.G[this.C++];
            if ("number" != typeof r)
                break;
            var i = Date.now();
            if (500 < i - this.R)
                return;
            this.R = i;
            try {
                this.e(r)
            } catch (e) {
                this.U = e,
                this.w && (this.C = this.w)
            }
        }
    }
    
    G.prototype.e = function(e) {
        var t = (61440 & e) >> 12;

    }
    (new G).v("AxjgB5MAnACoAJwBpAAAABAAIAKcAqgAMAq0AzRJZAZwUpwCqACQACACGAKcBKAAIAOcBagAIAQYAjAUGgKcBqFAuAc5hTSHZAZwqrAIGgA0QJEAJAAYAzAUGgOcCaFANRQ0R2QGcOKwChoANECRACQAsAuQABgDnAmgAJwMgAGcDYwFEAAzBmAGcSqwDhoANECRACQAGAKcD6AAGgKcEKFANEcYApwRoAAxB2AGcXKwEhoANECRACQAGAKcE6AAGgKcFKFANEdkBnGqsBUaADRAkQAkABgCnBagAGAGcdKwFxoANECRACQAGAKcGKAAYAZx+rAZGgA0QJEAJAAYA5waoABgBnIisBsaADRAkQAkABgCnBygABoCnB2hQDRHZAZyWrAeGgA0QJEAJAAYBJwfoAAwFGAGcoawIBoANECRACQAGAOQALAJkAAYBJwfgAlsBnK+sCEaADRAkQAkABgDkACwGpAAGAScH4AJbAZy9rAiGgA0QJEAJACwI5AAGAScH6AAkACcJKgAnCWgAJwmoACcJ4AFnA2MBRAAMw5gBnNasCgaADRAkQAkABgBEio0R5EAJAGwKSAFGACcKqAAEgM0RCQGGAYSATRFZAZzshgAtCs0QCQAGAYSAjRFZAZz1hgAtCw0QCQAEAAgB7AtIAgYAJwqoAASATRBJAkYCRIANEZkBnYqEAgaBxQBOYAoBxQEOYQ0giQKGAmQABgAnC6ABRgBGgo0UhD/MQ8zECALEAgaBxQBOYAoBxQEOYQ0gpEAJAoYARoKNFIQ/zEPkAAgChgLGgkUATmBkgAaAJwuhAUaCjdQFAg5kTSTJAsQCBoHFAE5gCgHFAQ5hDSCkQAkChgBGgo0UhD/MQ+QACAKGAsaCRQCOYGSABoAnC6EBRoKN1AUEDmRNJMkCxgFGgsUPzmPkgAaCJwvhAU0wCQFGAUaCxQGOZISPzZPkQAaCJwvhAU0wCQFGAUaCxQMOZISPzZPkQAaCJwvhAU0wCQFGAUaCxQSOZISPzZPkQAaCJwvhAU0wCQFGAkSAzRBJAlz/B4FUAAAAwUYIAAIBSITFQkTERwABi0GHxITAAAJLwMSGRsXHxMZAAk0Fw8HFh4NAwUABhU1EBceDwAENBcUEAAGNBkTGRcBAAFKAAkvHg4PKz4aEwIAAUsACDIVHB0QEQ4YAAsuAzs7AAoPKToKDgAHMx8SGQUvMQABSAALORoVGCQgERcCAxoACAU3ABEXAgMaAAsFGDcAERcCAxoUCgABSQAGOA8LGBsPAAYYLwsYGw8AAU4ABD8QHAUAAU8ABSkbCQ4BAAFMAAktCh8eDgMHCw8AAU0ADT4TGjQsGQMaFA0FHhkAFz4TGjQsGQMaFA0FHhk1NBkCHgUbGBEPAAFCABg9GgkjIAEmOgUHDQ8eFSU5DggJAwEcAwUAAUMAAUAAAUEADQEtFw0FBwtdWxQTGSAACBwrAxUPBR4ZAAkqGgUDAwMVEQ0ACC4DJD8eAx8RAAQ5GhUYAAFGAAAABjYRExELBAACWhgAAVoAQAg/PTw0NxcQPCQ5C3JZEBs9fkcnDRcUAXZia0Q4EhQgXHojMBY3MWVCNT0uDhMXcGQ7AUFPHigkQUwQFkhaAkEACjkTEQspNBMZPC0ABjkTEQsrLQ==")
    var b = function(e) {
        return __g._encrypt(encodeURIComponent(e))
    }
    exports.ENCRYPT_VERSION = A,
    exports.de = b
}

function encrypt(data) {
    var r = {exports: {}, i: 1}
    f(r, r.exports)
    return data
}
'''



'''js code'''
testcode = r'''
window = {
    navigator: {
        userAgent: "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36"
    }
}

function t(e) {
    return (t = "function" == typeof Symbol && "symbol" == typeof Symbol.A ? function(e) {
        return typeof e
    }
    : function(e) {
        return e && "function" == typeof Symbol && e.constructor === Symbol && e !== Symbol.prototype ? "symbol" : typeof e
    }
    )(e)
}

var A = "2.0",
__g = {};
function s() {}
function i(e) {
    this.t = (2048 & e) >> 11,
    this.s = (1536 & e) >> 9,
    this.i = 511 & e,
    this.h = 511 & e
}
function h(e) {
    this.s = (3072 & e) >> 10,
    this.h = 1023 & e
}
function a(e) {
    this.a = (3072 & e) >> 10,
    this.c = (768 & e) >> 8,
    this.n = (192 & e) >> 6,
    this.t = 63 & e
}
function c(e) {
    this.s = e >> 10 & 3,
    this.i = 1023 & e
}
function n() {}
function e(e) {
    this.a = (3072 & e) >> 10,
    this.c = (768 & e) >> 8,
    this.n = (192 & e) >> 6,
    this.t = 63 & e
}
function o(e) {
    this.h = (4095 & e) >> 2,
    this.t = 3 & e
}
function r(e) {
    this.s = e >> 10 & 3,
    this.i = e >> 2 & 255,
    this.t = 3 & e
}
s.prototype.e = function(e) {
    e.o = !1
}  
i.prototype.e = function(e) {
    switch (this.t) {
    case 0:
        e.r[this.s] = this.i;
        break;
    case 1:
        e.r[this.s] = e.k[this.h]
    }
}
h.prototype.e = function(e) {
    e.k[this.h] = e.r[this.s]
}    
a.prototype.e = function(e) {
    switch (this.t) {
    case 0:
        e.r[this.a] = e.r[this.c] + e.r[this.n];
        break;
    case 1:
        e.r[this.a] = e.r[this.c] - e.r[this.n];
        break;
    case 2:
        e.r[this.a] = e.r[this.c] * e.r[this.n];
        break;
    case 3:
        e.r[this.a] = e.r[this.c] / e.r[this.n];
        break;
    case 4:
        e.r[this.a] = e.r[this.c] % e.r[this.n];
        break;
    case 5:
        e.r[this.a] = e.r[this.c] == e.r[this.n];
        break;
    case 6:
        e.r[this.a] = e.r[this.c] >= e.r[this.n];
        break;
    case 7:
        e.r[this.a] = e.r[this.c] || e.r[this.n];
        break;
    case 8:
        e.r[this.a] = e.r[this.c] && e.r[this.n];
        break;
    case 9:
        e.r[this.a] = e.r[this.c] !== e.r[this.n];
        break;
    case 10:
        e.r[this.a] = t(e.r[this.c]);
        break;
    case 11:
        e.r[this.a] = e.r[this.c]in e.r[this.n];
        break;
    case 12:
        e.r[this.a] = e.r[this.c] > e.r[this.n];
        break;
    case 13:
        e.r[this.a] = -e.r[this.c];
        break;
    case 14:
        e.r[this.a] = e.r[this.c] < e.r[this.n];
        break;
    case 15:
        e.r[this.a] = e.r[this.c] & e.r[this.n];
        break;
    case 16:
        e.r[this.a] = e.r[this.c] ^ e.r[this.n];
        break;
    case 17:
        e.r[this.a] = e.r[this.c] << e.r[this.n];
        break;
    case 18:
        e.r[this.a] = e.r[this.c] >>> e.r[this.n];
        break;
    case 19:
        e.r[this.a] = e.r[this.c] | e.r[this.n];
        break;
    case 20:
        e.r[this.a] = !e.r[this.c]
    }
}
c.prototype.e = function(e) {
    e.Q.push(e.C),
    e.B.push(e.k),
    e.C = e.r[this.s],
    e.k = [];
    for (var t = 0; t < this.i; t++)
        e.k.unshift(e.f.pop());
    e.g.push(e.f),
    e.f = []
}
    
n.prototype.e = function(e) {
    e.C = e.Q.pop(),
    e.k = e.B.pop(),
    e.f = e.g.pop()
}
    
e.prototype.e = function(e) {
    switch (this.t) {
    case 0:
        e.u = e.r[this.a] >= e.r[this.c];
        break;
    case 1:
        e.u = e.r[this.a] <= e.r[this.c];
        break;
    case 2:
        e.u = e.r[this.a] > e.r[this.c];
        break;
    case 3:
        e.u = e.r[this.a] < e.r[this.c];
        break;
    case 4:
        e.u = e.r[this.a] == e.r[this.c];
        break;
    case 5:
        e.u = e.r[this.a] != e.r[this.c];
        break;
    case 6:
        e.u = e.r[this.a];
        break;
    case 7:
        e.u = !e.r[this.a]
    }
}
    
o.prototype.e = function(e) {
    switch (this.t) {
    case 0:
        e.C = this.h;
        break;
    case 1:
        e.u && (e.C = this.h);
        break;
    case 2:
        e.u || (e.C = this.h);
        break;
    case 3:
        e.C = this.h,
        e.w = null
    }
    e.u = !1
}
r.prototype.e = function(e) {
    switch (this.t) {
    case 0:
        for (var t = [], n = 0; n < this.i; n++)
            t.unshift(e.f.pop());
        e.r[3] = e.r[this.s](t[0], t[1]);
        break;
    case 1:
        for (var r = e.f.pop(), i = [], o = 0; o < this.i; o++)
            i.unshift(e.f.pop());
        e.r[3] = e.r[this.s][r](i[0], i[1]);
        break;
    case 2:
        for (var a = [], s = 0; s < this.i; s++)
            a.unshift(e.f.pop());
        e.r[3] = new e.r[this.s](a[0],a[1])
    }
}
var k = function(e) {
    for (var t = 66, n = [], r = 0; r < e.length; r++) {
        var i = 24 ^ e.charCodeAt(r) ^ t;
        n.push(String.fromCharCode(i)),
        t = i
    }
    return n.join("")
}
function Q(e) {
    this.t = (4095 & e) >> 10,
    this.s = (1023 & e) >> 8,
    this.i = 1023 & e,
    this.h = 63 & e
}
function C(e) {
    this.t = (4095 & e) >> 10,
    this.a = (1023 & e) >> 8,
    this.c = (255 & e) >> 6
}
function B(e) {
    this.s = (3072 & e) >> 10,
    this.h = 1023 & e
}
function f(e) {
    this.h = 4095 & e
}
function g(e) {
    this.s = (3072 & e) >> 10
}
function u(e) {
    this.h = 4095 & e
}
function w(e) {
    this.t = (3840 & e) >> 8,
    this.s = (192 & e) >> 6,
    this.i = 63 & e
}
function G() {
    this.r = [0, 0, 0, 0],
    this.C = 0,
    this.Q = [],
    this.k = [],
    this.B = [],
    this.f = [],
    this.g = [],
    this.u = !1,
    this.G = [],
    this.b = [],
    this.o = !1,
    this.w = null,
    this.U = null,
    this.F = [],
    this.R = 0,
    this.J = {
        0: s,
        1: i,
        2: h,
        3: a,
        4: c,
        5: n,
        6: e,
        7: o,
        8: r,
        9: Q,
        10: C,
        11: B,
        12: f,
        13: g,
        14: u,
        15: w
    }
}            
Q.prototype.e = function(e) {
    switch (this.t) {
    case 0:
        e.f.push(e.r[this.s]);
        break;
    case 1:
        e.f.push(this.i);
        break;
    case 2:
        e.f.push(e.k[this.h]);
        break;
    case 3:
        e.f.push(k(e.b[this.h]))
    }
}
    
C.prototype.e = function(A) {
    switch (this.t) {
    case 0:
        var t = A.f.pop();
        A.r[this.a] = A.r[this.c][t];
        break;
    case 1:
        var s = A.f.pop()
            , i = A.f.pop();
        A.r[this.c][s] = i;
        break;
    case 2:
        var h = A.f.pop();
        A.r[this.a] = eval(h)
    }
}
    
B.prototype.e = function(e) {
    e.r[this.s] = k(e.b[this.h])
}
    
f.prototype.e = function(e) {
    e.w = this.h
}
    
g.prototype.e = function(e) {
    throw e.r[this.s]
}
    
u.prototype.e = function(e) {
    var t = this
        , n = [0];
    e.k.forEach(function(e) {
        n.push(e)
    });
    var r = function(r) {
        var i = new G;
        return i.k = n,
        i.k[0] = r,
        i.v(e.G, t.h, e.b, e.F),
        i.r[3]
    };
    r.toString = function() {
        return "() { [native code] }"
    }
    ,
    e.r[3] = r
}
    
w.prototype.e = function(e) {
    switch (this.t) {
    case 0:
        for (var t = {}, n = 0; n < this.i; n++) {
            var r = e.f.pop();
            t[e.f.pop()] = r
        }
        e.r[this.s] = t;
        break;
    case 1:
        for (var i = [], o = 0; o < this.i; o++)
            i.unshift(e.f.pop());
        e.r[this.s] = i
    }
}
    
G.prototype.D = function(e) {
    for (var t = atob(e), n = t.charCodeAt(0) << 8 | t.charCodeAt(1), r = [], i = 2; i < n + 2; i += 2)
        r.push(t.charCodeAt(i) << 8 | t.charCodeAt(i + 1));
    this.G = r;
    for (var o = [], a = n + 2; a < t.length; ) {
        var s = t.charCodeAt(a) << 8 | t.charCodeAt(a + 1)
            , c = t.slice(a + 2, a + 2 + s);
        o.push(c),
        a += s + 2
    }
    this.b = o
}
    
G.prototype.v = function(e, t, n) {
    for (t = t || 0,
    n = n || [],
    this.C = t,
    "string" == typeof e ? this.D(e) : (this.G = e,
    this.b = n),
    this.o = !0,
    this.R = Date.now(); this.o; ) {
        var r = this.G[this.C++];
        if ("number" != typeof r)
            break;
        var i = Date.now();
        if (500 < i - this.R)
            return;
        this.R = i;
        try {
            this.e(r)
        } catch (e) {
            this.U = e,
            this.w && (this.C = this.w)
        }
    }
}
    
G.prototype.e = function(e) {
    var t = (61440 & e) >> 12;

}


var b = function(e) {

    return __g._encrypt(encodeURIComponent(e))

}

function encrypt(data) {

    return b(data)
}
'''


class ZhihuSpider(scrapy.Spider):
    name = 'zhihut'
    allowed_domains = ['zhihu.com']
    start_url = 'https://www.zhihu.com/'
    rules = (Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),)

    agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
    headers = {
        'Connection': 'keep-alive',
        'Host': 'www.zhihu.com',
        'Referer': 'https://www.zhihu.com/signin',
        'User-Agent': agent
        # 'authorization': 'oauth c3cef7c66a1843f8b3a9e6a1e3160e20'
    }
    header1 = {
        'content-type': 'application/x-www-form-urlencoded',
        "x-zse-83": "3_1.1",
        'Referer': 'https://www.zhihu.com/signin',
        'User-Agent': agent,
        'authorization': 'oauth c3cef7c66a1843f8b3a9e6a1e3160e20'
    }
    login_headers = {
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://www.zhihu.com',
        'referer': 'https://www.zhihu.com/signin',
        'x-requested-with': 'fetch',
        'x-zse-83': '3_2.0'
        }


    client_id='c3cef7c66a1843f8b3a9e6a1e3160e20'
    grant_type= 'password'
    source='com.zhihu.web'
    timestamp = str(int(time.time() * 1000))
    timestamp2 = str(time.time() * 1000)
    followee_ids = []
    ref_source = "homepage"
    captcha = ''



    # 处理签名
    def get_signnature(self,grant_type,client_id,source,timestamp):
        """
        通过 Hmac 算法计算签名
        固定字符串+时间戳
        """
        hm=hmac.new(b'd1b964811afb40118a12068ff74a12f4',None,sha1)
        hm.update(str.encode(grant_type))
        hm.update(str.encode(client_id))
        hm.update(str.encode(source))
        hm.update(str.encode(timestamp))
        return str(hm.hexdigest())

    def start_requests(self):
        yield scrapy.Request('https://www.zhihu.com/api/v3/oauth/captcha?lang=en',headers=self.headers,callback=self.start_login, meta={'cookiejar': 1},)  # meta={'cookiejar':1}

    def start_login(self,response):
        # 判断是否需要验证码
        need_cap=json.loads(response.body)['show_captcha']
        print(need_cap)
        if need_cap:
            print('需要验证码')
            yield scrapy.Request('https://www.zhihu.com/api/v3/oauth/captcha?lang=en',headers=self.headers,callback=self.capture,method='PUT', meta={'cookiejar': response.meta['cookiejar']})

        else:
            print('不需要验证码')
            post_url = 'https://www.zhihu.com/api/v3/oauth/sign_in'
            post_data ={
                'client_id': self.client_id,
                'grant_type': self.grant_type,
                'timestamp': self.timestamp,
                'source': self.source,
                'signature': self.get_signnature(self.grant_type, self.client_id, self.source, self.timestamp),
                'username': '账号',
                'password': '密码',
                'captcha': '',
                # 改为'cn'是倒立汉字验证码
                'lang': 'en',
                'ref_source': 'other_',
                'utm_source': ''}
            yield scrapy.FormRequest(url=post_url, formdata=post_data, headers=self.headers, meta={'cookiejar': response.meta['cookiejar']},)

    def capture(self,response):

        try:
            img = json.loads(response.body)['img_base64']
        except ValueError:
            print('获取img_base64值失败！')
        else:
            img = img.encode('utf8')
            img_data = base64.b64decode(img)

            with open('zhihu.gif', 'wb') as f:
                f.write(img_data)
                f.close()
        self.captcha = input('请输入验证码：')

        #继续发起一个post请求，获取验证码识别的是否正确
        yield scrapy.FormRequest(url='https://www.zhihu.com/api/v3/oauth/captcha?lang=en',
                                 callback=self.parse_post_captcha,
                                 formdata={
                                     'input_text':str(self.captcha)
                                     }, meta={'cookiejar': response.meta['cookiejar']})


    def parse_post_captcha(self,response):
        '''
        解析验证码的post请求，获取验证码的识别结果，输入的验证码是错误还是正确。
        :param response:
        :return:
        '''
        result=json.loads(response.text).get("success",'')
        if result:
            print('验证码输入正确')
            #访问这个sign_in这个url进行登录
            login_param={
                'client_id': self.client_id,
                'grant_type': self.grant_type,
                'source': self.source,
                'username':'18756967802',
                'password':'18756967802wang',
                'lang': 'en',
                'ref_source': 'other_https://www.zhihu.com/signin',
                'utm_source': '',
                'captcha': '',
                'timestamp': self.timestamp,
                'signature': self.get_signnature(self.grant_type, self.client_id, self.source, self.timestamp)
                }
            data = parse.urlencode(login_param)
            #post_data = self.myencrypt(login_param)
            post_data = 'aRR924_BFhoV-qoVp9VGS79hshoYi9omEqYhggHMcvOOsBOB8BF0g_LBXq2t3bO8xBF0g4eB2BNm2Lf8PqxGQJe8ST2t3bO8Ght06eUqb82po7Y0EqYhHUcmoqVOUu3q8Ln0QTrqSHtpcMtym_e0g4LmUbxOgqVGMTYhNr9qkXOfoMY08LtBNbuBkRFYnhFqMH2qHg9Bc7FpgutBsLO8Hv90k_LxgLNMs9V8EcL12BtxgTOBGbfGiqX1jbk9-qx9BLfBFUCG-qppkLPqMLF0cAuy2H2xbLY0EqYhQGL8eqoYJgxGMTYhHUcmoqVOUup9BLfBQqwGs9p9UhoBMTYhQ79BQ82x2LO0ZBYBbAe0nUtY2_tymXNqSHeqNCOf20x9BLPBDCpGECS_AqSw'

    	    #此时，需要现在settings.py文件中添加scrapy允许处理的状态码(即添加HTTPERROR_ALLOWED_CODES=[400,600])，因为scrapy默认只处理[200,300]之间的状态码。
            yield scrapy.FormRequest(
                    url='https://www.zhihu.com/api/v3/oauth/sign_in',
                    formdata=post_data,
                    method='POST',
                    callback=self.after_login,
                    headers=self.login_headers,
                    meta={'cookiejar': response.meta['cookiejar']}
                )

    def myencrypt(self, data):
        data = parse.urlencode(data)
        #testcode   encrypt_js_code
        ctx = execjs.compile(testcode)
        res = ctx.call('encrypt', data)
        return res;



    def after_login(self, response):
        if response.status == 200:
            print("登录成功")

        else:
            print("登录失败")



