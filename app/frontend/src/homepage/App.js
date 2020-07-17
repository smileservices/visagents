import ReactDOM from "react-dom";
import React, {useEffect, useState} from "react";
import {QuoteForm} from "./Form"
import {ProspectForm} from "./ProspectForm";

function App() {
    const [showProspectForm, setShowProspectForm] = useState(false)
    const [countryList, setCountryList] = useState([]);
    const [servicesList, setServicesList] = useState([]);
    const [citiesList, setCitiesList] = useState([]);

    function get_countries() {
        fetch(DATA_ENDPOINT.countries, {
            method: "GET"
        }).then(result => {
            //todo set waiting
            if (result.ok) {
                return result.json();
            } else {
                setAlert('Could not read data: ' + result.statusText)
            }
        }).then(data => {
            setCountryList(data);
        })
    }

    function get_cities() {
        fetch(DATA_ENDPOINT.cities, {
            method: "GET"
        }).then(result => {
            //todo set waiting
            if (result.ok) {
                return result.json();
            } else {
                setAlert('Could not read data: ' + result.statusText)
            }
        }).then(data => {
            setCitiesList(data);
        })
    }

    function get_services() {
        fetch(DATA_ENDPOINT.services, {
            method: "GET"
        }).then(result => {
            //todo set waiting
            if (result.ok) {
                return result.json();
            } else {
                setAlert('Could not read data: ' + result.statusText)
            }
        }).then(data => {
            setServicesList(data);
        })
    }

    useEffect(() => {
        get_countries();
        get_cities();
        get_services();
    }, [])

    if (!showProspectForm) return (
        <div className="row">
            <div className="col-md-6">
                <h2 className="heading mb-3">Get quote from 50+ visa agencies in Vietnam</h2>
                <div className="sub-heading">
                    <p className="mb-4">
                        Submit a request for visa services using the form and get quoted from visa agencies directly
                        to your email
                    </p>
                    <p className="mb-5"><a className="btn btn-success btn-lg pb_btn-pill smoothscroll"
                                           href="#" onClick={e=>{e.preventDefault(); setShowProspectForm(true)}}><span
                        className="pb_font-14 text-uppercase pb_letter-spacing-1">Are you a visa agency?</span></a>
                    </p>
                </div>
            </div>
            <div className="col-md-1">
            </div>
            <div className="col-md-5 relative align-self-center">
                <QuoteForm countryList={countryList} servicesList={servicesList} citiesList={citiesList}/>
            </div>
        </div>
    );

    return (
        <div className="row">
            <div className="col-md-6">
                <h2 className="heading mb-3">Register your visa agency for free</h2>
                <div className="sub-heading">
                    <p className="mb-4">
                        Fill in the form and start receiving visa services requests from expats. It's free!
                    </p>
                    <p className="mb-5"><a className="btn btn-success btn-lg pb_btn-pill smoothscroll"
                                           onClick={e=>{e.preventDefault(); setShowProspectForm(false)}}><span
                        className="pb_font-14 text-uppercase pb_letter-spacing-1">Are you an expat?</span></a>
                    </p>
                </div>
            </div>
            <div className="col-md-1">
            </div>
            <div className="col-md-5 relative align-self-center">
                <ProspectForm citiesList={citiesList} />
            </div>
        </div>
    );
}

const wrapper = document.getElementById("app");
wrapper ? ReactDOM.render(<App/>, wrapper) : null;