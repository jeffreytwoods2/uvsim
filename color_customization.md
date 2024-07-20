### Detailed Instructions:

1. **Understanding Color Codes:**
   - Colors in the app are represented by "Hex color codes".
   - These codes always start with a "#" followed by 6 characters.
   - Example: "#15905b" is a shade of green.

2. **Choosing New Colors:**
   - We recommend using a color picker tool to find hex codes for your preferred colors.
   - Try this websites: [HTML Color Picker](https://www.w3schools.com/colors/colors_picker.asp) or [Image Color Picker](https://imagecolorpicker.com/color-code/15905b) 
   - Pick a color you like and copy the "Hex" value (it starts with #).

3. **Modifying the theme.json File:**
  
   - Open `theme.json` in a simple text editor like Notepad or VS Code.
   - Find the color you want to change. For example:
     ```json
     "CTkButton": {
       "fg_color": ["#15905b", "#15905b"],
     ```
   - Replace the color code with your new one:
     ```json
     "CTkButton": {
       "fg_color": ["#15905b", "#FF5733"],
     ```
   - This would change the button color to a bright orange.

4. **Tips:**
   - Keep the format intact: Always use the "#" symbol followed by 6 characters.
   - Some items have two color codes in square brackets `[ ]`. These are for light and dark modes. Note that the current theme is set to dark but you can set them to the same color if you're unsure.
   - After making changes, save the file and restart the app to see your new color scheme.
  
5. **Color Locations in theme.json:**

   *Main Elements:*
   - `CTkFrame`: This controls the main background of the app.
   - `CTkButton`: This determines the appearance of buttons.
   - `CTkLabel`: This sets the text color for labels.
   - `CTkTextbox`: This manages the colors for text boxes.
   
   *Color Properties:*
   - `fg_color`: This sets the background color.
   - `hover_color`: This determines the color when you move your mouse over the element (mainly for buttons).
   - `text_color`: This controls the color of the text.
   - `border_color`: While our app doesn't use borders, don't remove this property. Changing it won't affect the app's appearance, but deleting it might cause issues.

Remember: When changing colors, always keep the `"` quotation marks around the color codes, and don't remove any commas or brackets.
Also, if something goes wrong, you can always revert to the original `theme.json` file!
