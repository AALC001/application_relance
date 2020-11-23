

class Card extends React.Component {
    constructor(props){
        super(props)
        this.state = {
            count: 0
          };
    }
    

    componentDidMount() {
        const countPatientURL = document.querySelector(".dash-section [type='hidden']")

        fetch(countPatientURL.value)
        .then(res => res.json())
        .then(data => {
            this.setState({
                count: data.data.count
            })
        }).catch(err => console.log(err))
    }

    render() {
        const format_count = new Intl.NumberFormat("en-US", {maximumFractionDigits: 3}).format(this.state.count)
        return <p>{format_count}</p>
    }
}