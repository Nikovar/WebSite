import React, {Component} from 'react';
import { SymbolNavigation, PageWindow } from "./components"
import { Row, Col } from 'react-bootstrap';


class Main extends Component {
    render() {
        return(
            <div className='container'>
                <Row>
                    <Col sm={4}>
                        <SymbolNavigation />
                    </Col>
                    <Col sm={8}>
                        <PageWindow />
                    </Col>
                </Row>
            </div>
        )
    }
}

export default Main;
