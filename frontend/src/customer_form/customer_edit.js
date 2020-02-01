import CustomerForm from 'customer_form/customer_form';
import {
    withRouter
} from 'react-router-dom';
import {
    omit,
    pick,
} from 'lodash';
import API from 'common/api';

class CustomerEdit extends CustomerForm {
    constructor(prop) {
        super(prop)
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    componentDidMount() {
        const { match: { params } } = this.props;
        API.get(`customers/${params.id}`)
            .then(res => this.setState(pick(res.data, [
                'first_name',
                'last_name',
                'address1',
                'address2',
                'city',
                'state',
                'code',
            ])))
    }

    handleSubmit(event) {
        const { match: { params } } = this.props;
        API.post(`customers/${params.id}`, omit(this.state, 'errors'))
            .then(res => {
                this.props.history.push(`/${res.data.id}`)
            })
            .catch(error => {
                this.setState({
                    errors: error.response.data
                })
            })
        event.preventDefault();
    }
}

export default withRouter(CustomerEdit)