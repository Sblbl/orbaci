$(window).on('load', function() {
	let $_wfield = $('#w_config'),
		$_hfield = $('#h_config'),
		side = 32

	let current_w = 0,
		current_h = 0


	function drawRects() {
		$('#pattern').remove()
		w = $_wfield.val()
		h = $_hfield.val()

		let svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg')

	    $_svg = $(svg)
	    $_svg.attr({'id': 'pattern', 'width' : w*side, 'height' : h*side})

	    let counter = 0

		for (let y=0; y<h; y++) {
			for  (let x=0; x<w; x++) {
				let rect = document.createElementNS('http://www.w3.org/2000/svg', 'rect')
				let $_r = $(rect).attr({
					'id' : `${x}_${y}`,
					'class' : 'dot', 
					'x' : side*x,
					'y' : side*y, 
					'width' : side,
					'height' : side
				})

				$_svg.append($_r)
				counter ++
			}
		}

		current_w = w
		current_h = h

		$('#pattern_container').append($_svg)

		$('.dot').on('click', (e) => {
			$(e.target).toggleClass('black')
			makeTranscript()
		})

		makeTranscript()
	}

	function makeTranscript() {

		let $_transcr = $('#pattern_transcript')
		$_transcr.empty()
		
		for (let y=0; y<current_h; y++) {
			let p = document.createElement('span')
			let transcript = ''
			
			for (let x=0; x<current_w; x++) {
				let $_r = $(`#${x}_${y}`)
				let val = ($_r.hasClass('black') ? '1' : '0')
				transcript += val 
				transcript += ', '
			}

			$_p = $(p)
			$_p.html(transcript.slice(0, -2))
			$_transcr.append($_p)
		}

	}

	$_wfield.val(2)
	$_hfield.val(2)

	drawRects()

	$('#draw_button').on('click', (e) => {
		drawRects()
	})

})