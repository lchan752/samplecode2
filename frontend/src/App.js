import React from 'react';
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link,
} from 'react-router-dom';
import 'App.scss';
import CustomerList from 'customer_list/customer_list';
import CustomerDetail from 'customer_detail/customer_detail';
import CustomerCreate from 'customer_form/customer_create';
import CustomerEdit from 'customer_form/customer_edit';

export default function App() {
  return (
    <Router>
      <div className='topbar'>
        <h3><Link to='/'>Samplecode</Link></h3>
      </div>
      <div className='container'>
        <Switch>
          <Route path='/' exact component={CustomerList}></Route>
          <Route path="/create/" exact component={CustomerCreate}></Route>
          <Route path="/edit/:id" component={CustomerEdit}></Route>
          <Route path="/:id" component={CustomerDetail}></Route>
        </Switch>
      </div>
    </Router>
  )
}