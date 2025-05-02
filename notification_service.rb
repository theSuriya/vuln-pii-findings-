require 'net/smtp'

def send_notification(user)
  message = <<~MESSAGE_END
    From: Support <support@myapp.com>
    To: #{user[:email]}
    Subject: Password Reset

    Hi #{user[:name]},
    We have reset your password as per your request.
    Please use this temporary password: tmpP@ssw0rd123

    If you did not request this, contact us at +1-800-555-0199.
  MESSAGE_END

  Net::SMTP.start('smtp.example.com', 25) do |smtp|
    smtp.send_message message, 'support@myapp.com', user[:email]
  end
end

# Example invocation
user = { name: 'Dana Scully', email: 'dana.scully@fbi.gov' }
send_notification(user)