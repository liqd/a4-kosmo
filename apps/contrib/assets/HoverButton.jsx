import React, { useState, useEffect } from 'react'

export const HoverButton = (props) => {
  const [buttonText, setButtonText] = useState(props.text)

  useEffect(() => {
    setButtonText(props.text)
  }, [props.text])

  return (
    <button
      id={props.id}
      className={props.className}
      type="button"
      onClick={props.onClick}
      disabled={props.disabled}
      onMouseEnter={() => setButtonText(props.hoverText)}
      onMouseLeave={() => setButtonText(props.text)}
      aria-label={buttonText}
    >
      {props.icon}
      <span className="ms-1">
        {buttonText}
      </span>
    </button>
  )
}
