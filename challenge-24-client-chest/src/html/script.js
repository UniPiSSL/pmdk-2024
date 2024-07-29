
(function(){
	window.say = (text, style='') => {
		let say = document.getElementById("say");
		say.textContent = text;
		console.log(style);
		say.className = style;
	}
	window.checkPassword = () => {
		var guess = document.getElementById("password").value;

		if (guess == secret) {
			let flag = getFlag(guess);
			if (flag) say(flag, 'correct');
		} else {
			say((array => array[Math.floor(Math.random() * array.length)])([
				'Η σοφία είναι ένα κλειδί που ψάχνεις, νέε μου. Συνεχίστε την αναζήτηση.',
				'Ο δρόμος προς τη σοφία είναι γεμάτος αποτυχίες. Κρατήστε την αντοχή σου και προχωρήσε.',
				'Κάθε αποτυχία είναι ένα βήμα προς τη σωστή κατεύθυνση. Μην πτοείσε.',
				'Κάθε λάθος είναι ένα μάθημα, κάθε αποτυχία είναι ένα βήμα προς τη γνώση.',
				'Στο ταξίδι για την κατανόηση, ακόμη και η αποτυχία φέρνει φως. Συνεχίστε να φωτίζετε τον δρόμο σας.',
				'Η λύση είναι κάπου μέσα στο χάος των ερωτημάτων. Συνεχίστε την αναζήτησή σας.'
			]), 'wrong');
		}
	}
})();

(function(w){
	let a = 'c2VjcmV0';
	let ator = (x => atob(x).split("").reverse().join(""));
	w[atob(a)] = JSON.parse(atob('eyJpIjoibm9wIiAgICAgICAgICAgIH0=')).i;
	w[ator(a)] = JSON.parse(atob('eyJpIjoidzFzZDBtXzFzX1Awd2VSIn0=')).i;
	((i) => {
		w[i] = ((i, j) => {
			return () => {
				w[atob(a)] = w[ator(a)];
				i();
				w[atob(a)] = j;
			};
		})(w[i], w[atob(a)]);
	})(atob('Y2hlY2tQYXNzd29yZA=='));

	window[atob('Z2V0RmxhZw==')] = () => {
		return w[atob('c2F5')](atob('VGFtcGVyaW5nIERldGVjdGVkIQ=='));
	}
	let x = (n, m) => {
		let e = new TextEncoder();
		n = e.encode(n);
		m = e.encode(m);
		n = n.map((b, i) => b ^ m[i%m.length]);
		return new TextDecoder('utf-8').decode(new Uint8Array(n));
	}
	let i = new Image();
	i.onload = () => {
		try {
			let c = document.createElement("canvas").getContext("2d");
			c.drawImage(i, 0, 0);
			c.getImageData(0, 0, i.width, i.height);
			window[atob('Z2V0RmxhZw==')] = (y => x('1}2#K\tlG^+`\x00\x1BP\x7F\x07CCI_?r{ r8\x04\x14.7%\x0E\x0E', y));
		} catch (e) {};
	};
	i.src = document.querySelector('img').src;
})(window);
