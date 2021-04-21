const audio_file_types = ['mp3']

class AudioTypeForm extends React.Component {

	render() {
		return (
			<div id="react">
				<label for="audio_file_type" id="audio-file-type">Audio File Types: &nbsp; </label>
				<select name="audio_file_types" id="audio_file_type">
					{audio_file_types.map(audio_file_type =>
						<option value={audio_file_type}>{audio_file_type}</option>
					)}
				</select>
			</div>
		)
	}
}

ReactDOM.render(
	<AudioTypeForm/>,
	document.getElementById('react-component')
)