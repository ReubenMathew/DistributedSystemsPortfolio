<template>
  <div>
    <h1>Reuben Ninan</h1>
    <p>Currently Listening To: {{ track }}</p>
  </div>
</template>

<script>
import axios from 'axios'

export default {
	data () {
	    return {
	    	track: ''
	    }
  	}, methods: {
		getTrack() {
			this.track = this.getTrackFromBackend()
		},
		getTrackFromBackend() {
		    axios.get('http://localhost:8000/api/spotify')
		    .then(response => {
		    	this.track = response.data.curr
		    	console.log(response);
		    })
		    .catch(error => {
		    	console.log(response);
		    	console.log(error)
		    })
	  	}
	}, created () {
	    this.getTrack(),
	    this.getTrackFromBackend()
  }
}

</script>