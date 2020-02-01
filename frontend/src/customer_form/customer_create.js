import CustomerForm from 'customer_form/customer_form';
import {
    withRouter
} from 'react-router-dom';
import {
    omit,
} from 'lodash';
import API from 'common/api';

class CustomerCreate extends CustomerForm {
    constructor(prop) {
        super(prop)
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    handleSubmit(event) {
        API.post("customers/", omit(this.state, 'errors'))
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

export default withRouter(CustomerCreate)