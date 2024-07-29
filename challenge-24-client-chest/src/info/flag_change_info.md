
```javascript
let x = (n, m) => {
	let e = new TextEncoder();
	n = e.encode(n);
	m = e.encode(m);
	n = n.map((b, i) => b ^ m[i%m.length]);
	return new TextDecoder('utf-8').decode(new Uint8Array(n));
}

result_to_replace_in_code = x('FLAG{here}', 'w1sd0m_1s_P0weR')
```
