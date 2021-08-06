$(window).on('load', function() {
	let $_wfield = $('#w_config'),
		$_hfield = $('#h_config'),
		side = 32

	let current_w = 0,
		current_h = 0,
		mode = 'black',
		drawing = false

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

		$('.dot').on('mousemove', (e) => {
			if (mode == 'black' && drawing) {
				$(e.target).addClass('black')	
			} else if (mode == 'white' && drawing){
				$(e.target).removeClass('black')	
			}
			
			makeTranscript()
		})

		$('.dot').on('click', (e) => {
			if (mode == 'black') {
				$(e.target).addClass('black')	
			} else if (mode == 'white'){
				$(e.target).removeClass('black')	
			}
			
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

	$_wfield.val(6)
	$_hfield.val(6)

	drawRects()

	$('#draw_button').on('click', (e) => {
		drawRects()
	})

	$('.palette_button').on('click', (e) => {
		let $_target = $(e.target)
		if(e.target.nodeName != 'BUTTON') {
			$_target = $(e.target).parent()
		} 
		$('.palette_button').removeClass('current')
		$_target.addClass('current')

		mode = $_target.attr('mode')
	})

	$(document).on('mousedown', e => {
		drawing = true
	})

	$(document).on('mouseup', e => {
		drawing = false
	})

})