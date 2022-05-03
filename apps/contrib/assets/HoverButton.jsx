import React, { useState } from 'react'

export const HoverButton = (props) => {
  const [buttonText, setButtonText] = useState(props.children.text)

  return (
    <button
      id={props.id}
      className={props.className}
      type="button"
      onClick={props.onClick}
      disabled={props.disabled}
      onMouseEnter={() => setButtonText(props.children.hoverText)}
      onMouseLeave={() => setButtonText(props.children.text)}
      aria-label={buttonText}
    >
      {props.children.icon}
      <span className="ms-1">
        {buttonText}
      </span>
    </button>
  )
}
