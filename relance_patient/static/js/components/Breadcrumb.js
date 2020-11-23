
'use strict';

const Breadcrumb = ({items}) => {
    const renderItems = items.map((item, index) => {
        if(items.length - 1 === index) {
            return <li key={index} className="breadcrumb__item">{item.name}</li>
        }
        return <li key={index} className="breadcrumb__item"><a href={item.link} className="breadcrumb__link">{item.name}</a></li>
    });

    return (
        <div className="breadcrumb">
            <ul className="breadcrumb__list">
                {renderItems.map(element => element)}
            </ul>
        </div>
    )
}
