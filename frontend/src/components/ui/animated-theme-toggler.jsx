"use client"

import { useCallback, useEffect, useRef, useState } from 'react'
import { flushSync } from 'react-dom'
import { AnimatePresence, motion } from 'framer-motion'
import { Moon, Sun } from 'lucide-react'

import { cn } from '@/lib/utils'

export const AnimatedThemeToggler = ({ className }) => {
  const buttonRef = useRef(null)
  const [darkMode, setDarkMode] = useState(() =>
    typeof window !== 'undefined'
      ? document.documentElement.classList.contains('dark')
      : false,
  )

  useEffect(() => {
    const syncTheme = () =>
      setDarkMode(document.documentElement.classList.contains('dark'))

    const observer = new MutationObserver(syncTheme)
    observer.observe(document.documentElement, {
      attributes: true,
      attributeFilter: ['class'],
    })
    return () => observer.disconnect()
  }, [])

  const onToggle = useCallback(async () => {
    if (!buttonRef.current) return

    const previousBackground = getComputedStyle(document.body).backgroundColor
    const rootElement = document.getElementById('root')
    const { left, top, width, height } = buttonRef.current.getBoundingClientRect()
    const centerX = left + width / 2
    const centerY = top + height / 2
    const maxDistance = Math.hypot(
      Math.max(centerX, window.innerWidth - centerX),
      Math.max(centerY, window.innerHeight - centerY),
    )

    const overlay = document.createElement('div')
    overlay.style.position = 'fixed'
    overlay.style.inset = '0'
    overlay.style.pointerEvents = 'none'
    overlay.style.zIndex = '9999'
    overlay.style.overflow = 'hidden'
    overlay.style.background = previousBackground
    overlay.style.clipPath = `circle(${maxDistance}px at ${centerX}px ${centerY}px)`

    // Freeze current theme tokens on the overlay so the snapshot stays in the old theme.
    const computedRoot = getComputedStyle(document.documentElement)
    for (let index = 0; index < computedRoot.length; index += 1) {
      const property = computedRoot[index]
      if (!property.startsWith('--')) continue
      overlay.style.setProperty(property, computedRoot.getPropertyValue(property))
    }

    if (rootElement) {
      const clonedRoot = rootElement.cloneNode(true)
      clonedRoot.setAttribute('aria-hidden', 'true')
      overlay.appendChild(clonedRoot)
    }

    document.body.appendChild(overlay)

    const applyTheme = () => {
      flushSync(() => {
        const toggled = !darkMode
        setDarkMode(toggled)
        document.documentElement.classList.toggle('dark', toggled)
        localStorage.setItem('theme', toggled ? 'dark' : 'light')
      })
    }

    applyTheme()

    const appWideAnimation = overlay.animate(
      {
        clipPath: [
          `circle(${maxDistance}px at ${centerX}px ${centerY}px)`,
          `circle(0px at ${centerX}px ${centerY}px)`,
        ],
      },
      {
        duration: 700,
        easing: 'ease-in-out',
      },
    )

    await appWideAnimation.finished.catch(() => {})
    overlay.remove()
  }, [darkMode])

  return (
    <button
      ref={buttonRef}
      onClick={onToggle}
      aria-label="Switch theme"
      className={cn(
        'flex items-center justify-center rounded-full p-2 outline-none focus:outline-none active:outline-none focus:ring-0 cursor-pointer',
        className,
      )}
      type="button"
    >
      <AnimatePresence mode="wait" initial={false}>
        {darkMode ? (
          <motion.span
            key="sun-icon"
            initial={{ opacity: 0, scale: 0.55, rotate: 25 }}
            animate={{ opacity: 1, scale: 1, rotate: 0 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.33 }}
            className="text-white"
          >
            <Sun />
          </motion.span>
        ) : (
          <motion.span
            key="moon-icon"
            initial={{ opacity: 0, scale: 0.55, rotate: -25 }}
            animate={{ opacity: 1, scale: 1, rotate: 0 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.33 }}
            className="text-black"
          >
            <Moon />
          </motion.span>
        )}
      </AnimatePresence>
    </button>
  )
}
